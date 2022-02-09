from payment.models import PaymentType, Payment, Agency2Woman2PaymentType
from rest_framework import viewsets

from payment.serializers import PaymentTypeSerializer, PaymentSerializer, Agency2Woman2PaymentTypeSerializer


class AdminPaymentTypeView(viewsets.ModelViewSet):
    serializer_class = PaymentTypeSerializer
    queryset = PaymentType.objects.all()


class AdminPaymentView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class AdminAgency2Woman2PaymentTypeView(viewsets.ModelViewSet):
    serializer_class = Agency2Woman2PaymentTypeSerializer
    queryset = Agency2Woman2PaymentType.objects.all()
