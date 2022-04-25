from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from payment.models import Payment
from settings.models import ReplanishmentPlan, Pictures
from rest_framework.response import Response
from account.models import ReplenishmentLog
from backend.local import DOMAIN



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
