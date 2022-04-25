from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from account.models import ReplenishmentLog, UserProfile

from subscription.models import BonusSubscription


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Load ReplanishmentLog...')
        ReplenishmentLog.objects.all().delete()
        up_objs = UserProfile.objects.all()
        bs_objs = BonusSubscription.objects.all()

        objs = []

        for u_obj in up_objs[:10]:
            for bs in bs_objs:
                objs.append(ReplenishmentLog(user_profile=u_obj, bonus_subscription=bs))
        ReplenishmentLog.objects.bulk_create(objs)
        print('ok')
