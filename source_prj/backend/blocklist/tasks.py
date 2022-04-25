from backend.celery import app
from django.utils import timezone


@app.task
def unblock_users():
    from blocklist.models import BlockList
    month_before = timezone.datetime.now() - timezone.timedelta(days=30)
    BlockList.objects.filter(created_at__lt=month_before).delete()
