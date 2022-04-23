from django.db import models
from django.contrib.auth.models import User
from account.models import UserProfile


class BlockList(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blocked_profiles', null=True)
    block_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='block_by_user', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = 'profile', 'block_by_user'
