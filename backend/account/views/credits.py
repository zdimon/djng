from rest_framework.views import APIView
from rest_framework.response import Response
from payment.tasks import update_account_service
from account.user_serializer import ShortUserSerializer
from account.models import ReplenishmentLog, ReplanishmentPlan
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

class ReplenishmentLogSerializer(serializers.ModelSerializer):
    credits = serializers.CharField(required=False, allow_blank=True, max_length=100)
    class Meta:
        model = ReplenishmentLog
        fields = ['id', 'credits'] 


class AddCretitsView(CreateAPIView):
    """
       Add credits POST 
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ReplenishmentLogSerializer
    def post(self, request, format=None):
        plan = ReplanishmentPlan.objects.get(name="45 $")
        pr = request.user.userprofile
        pr.account = pr.account + int(request.data.get('credits'))
        pr.save()
        log = ReplenishmentLog()
        log.user_profile = pr
        log.plan = plan
        log.save()

        update_account_service(pr)
        return Response(ReplenishmentLogSerializer(log).data)