from celery import shared_task
from .models import OtpCode
from datetime import datetime,timedelta
import pytz


@shared_task
def delete_expired_codes():
    """
    Delete all expired otp codes by celery beat
    """
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
    OtpCode.objects.filter(created__lt=expired_time).delete()


