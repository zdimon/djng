from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from payment.models import Payment
from settings.models import ReplanishmentPlan, Pictures
from rest_framework.response import Response
from account.models import ReplenishmentLog
from backend.local import DOMAIN
from rest_framework import generics, viewsets, status
from settings.models import ReplanishmentPlan
from settings.serializers import ReplanishmentPlanSerializer

class PlanViewSet(viewsets.ModelViewSet):
    queryset = ReplanishmentPlan.objects.all()
    serializer_class = ReplanishmentPlanSerializer
    lookup_field = 'id'
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)    
    def bulkDelete(self, request, *args, **kwargs):
        for i in request.data['itemsIdsForDelete']:
            l = ReplanishmentPlan.objects.get(pk=i)
            l.delete()
        response = {'status': 0, 'message': 'Ok'}
        return Response(response)

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
