from django.db import models

from account.models import UserProfile
from payment.models import PaymentType


class BonusSubscription(models.Model):
    BONUSES_LEVELS = (
        (0, 'basic'),
        (1, 'normal'),
        (2, 'best')
    )

    bonus_level = models.CharField(choices=BONUSES_LEVELS, max_length=10, default=0)
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        self.expire_at
        return True


class BonusSubscription2PaymentType(models.Model):
    """
    one time, two times etc. or duration in minutes
    """
    LIMIT_MEASUREMENTS = (('times', 'times (usage counts)'),
                          ('duration', 'duration (minutes)'))

    bonus_subscription = models.ForeignKey(BonusSubscription, related_name='services', on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType,  on_delete=models.CASCADE)
    limit = models.FloatField(default=0)
    # todo move to PaymentType?
    limit_units = models.CharField(choices=LIMIT_MEASUREMENTS, max_length=15, default='times')
    created_at = models.DateTimeField(auto_now_add=True)


    def get_limit(self):
        return f'current limit for {self.payment_type.alias} is {self.limit} {self.limit_units}'

    # UserProfile -> ReplanishamentLog -> BonusSubscription -> BonusSubscription2PaymentType #1
                                                        #  \-> BonusSubscription2PaymentType #2
                                                        #   \-> BonusSubscription2PaymentType #n


class BonusSubscriptionUsedLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    used_service = models.ForeignKey(BonusSubscription2PaymentType, on_delete=models.CASCADE)
    how_much = models.FloatField(default=.0)
    created_at = models.DateTimeField(auto_now_add=True)
