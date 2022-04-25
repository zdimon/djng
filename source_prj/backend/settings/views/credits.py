from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from payment.models import Payment
from settings.models import ReplanishmentPlan, Pictures
from rest_framework.response import Response
from account.models import ReplenishmentLog
from backend.local import DOMAIN


class AddCreditsView(APIView):
    """
       Replanishment plan
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        plan = ReplanishmentPlan.objects.get(id=request.data['plan_id'])

        out = {
            'plan_id': plan.id,
            'credits': plan.credit
        }
        pr = request.user.userprofile
        pr.account = pr.account + int(request.data['credits'])
        pr.save()

        try:
            log = ReplenishmentLog.objects.get(user_profile=pr)
            # prolong subscription
            if log.bonus_subscription and log.bonus_subscription.is_active():
                log.pk = None
                log.bonus_subscription = max(plan.bonus_subscription, log.plan.bonus_subscription,
                                             key=lambda x: x.bonus_level)
        except ReplenishmentLog.DoesNotExist:
            log = ReplenishmentLog(user_profile=pr)
            log.bonus_subscription = plan.bonus_subscription
        log.plan = plan
        log.save()

        sub_payment_logs = []
        for pt in log.bonus_subscription.services.all():
            pm = Payment(sub=log.bonus_subscription, type=pt, payer=pr)
            sub_payment_logs.append(pm)
        Payment.objects.bulk_create(sub_payment_logs)

        return Response(out)

