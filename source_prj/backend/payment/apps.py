from django.apps import AppConfig
from payment.models import PaymentType

class ChargingConfig(AppConfig):
    name = 'payment'
    verbose_name = 'pay'
