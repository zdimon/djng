import random

from django.core.management.base import BaseCommand, CommandError

from payment.models import PaymentType, Agency2Woman2PaymentType, Payment
from agency.models import Agency2Woman


def create_objs_agency_woman_payments_type(payment_type_objs):
    ag_2_w_payment_types = []
    for agency_woman in Agency2Woman.objects.all():
        for payment_type in payment_type_objs:
            ag_2_w_payment_type = Agency2Woman2PaymentType(agency=agency_woman.agency, woman=agency_woman.woman,
                                                           payment_type=payment_type)
            ag_2_w_payment_types.append(ag_2_w_payment_type)
    return ag_2_w_payment_types


class Command(BaseCommand):
    """
    aliases of payment type
    """
    payment_aliases = ('text-chat', 'video-chat', 'photo-in-chat', 'show-hidden-photo', 'show-hidden-video',
                       'video-in-chat', 'contacts', 'sticker'
                       )
    prices = 1, 2, 3, 4, 5, 6, 7, 8

    def handle(self, *args, **options):
        print('Load Payment types...')
        Payment.objects.all().delete()
        PaymentType.objects.all().delete()
        payment_type_objs = []
        for pk, (alias, price) in enumerate(zip(self.payment_aliases, random.sample(self.prices, 8))):
            payment_type_objs.append(PaymentType(pk=pk, alias=alias, price=price, name=f'Charging for the {alias}'))

        obj_list = PaymentType.objects.bulk_create(payment_type_objs)
        ag_2_w_payment_types = create_objs_agency_woman_payments_type(obj_list)
        Agency2Woman2PaymentType.objects.bulk_create(ag_2_w_payment_types)
        print('ok')
