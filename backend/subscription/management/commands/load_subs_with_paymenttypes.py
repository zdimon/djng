import random
from django.core.management.base import BaseCommand, CommandError

from subscription.models import BonusSubscription2PaymentType, BonusSubscription

from payment.models import PaymentType


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Load BonusSubscription2PaymentType...')
        BonusSubscription2PaymentType.objects.all().delete()
        bs_objs = BonusSubscription.objects.all()
        pt_objs = PaymentType.objects.all()

        objs = []
        for bs in bs_objs:
            for pt in pt_objs:
                obj = BonusSubscription2PaymentType(bonus_subscription=bs, payment_type=pt,
                                                    limit=float(random.randint(1, 20)),
                                                    limit_measurement=random.choices(['times', 'duration'])[0])
                objs.append(obj)
        BonusSubscription2PaymentType.objects.bulk_create(objs)
        print('ok')
