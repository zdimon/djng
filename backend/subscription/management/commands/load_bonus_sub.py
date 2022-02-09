from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from subscription.models import BonusSubscription


class Command(BaseCommand):
    subs_levels = 0, 1, 2

    def handle(self, *args, **options):
        print('Load BonusSubscription...')
        BonusSubscription.objects.all().delete()
        objs = []
        for lvl in self.subs_levels:
            objs.append(BonusSubscription(bonus_level=lvl, expire_at=timezone.now()))
        BonusSubscription.objects.bulk_create(objs)
        print('ok')
