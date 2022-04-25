from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from payment.models import Payment
from .models import ReplanishmentPlan, Pictures
from rest_framework.response import Response
from account.models import ReplenishmentLog
from backend.local import DOMAIN


class ReplanishmentPlanView(APIView):
    """
       Replanishment plan
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        plan = ReplanishmentPlan.objects.all().order_by('-dollar')
        out = []
        for i in plan:
            out.append({
                'id': i.id,
                'name': i.name,
                'dollar': i.dollar,
                'credit': i.credit
            })
        return Response(out)


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


class SmilesListView(APIView):
    """
       List of smiles
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        pics = Pictures.objects.filter(type_obj='smile')
        out = []
        for p in pics:
            out.append({
                "image": DOMAIN + p.image.url,
                "alias": p.alias,
                "name": p.name
            })
        return Response(out)


class StickersListView(APIView):
    """
       List of stickers
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        pics = Pictures.objects.filter(type_obj='sticker')
        out = []
        for p in pics:
            out.append({
                "image": DOMAIN + p.image.url,
                "name": p.name
            })
        return Response(out)
