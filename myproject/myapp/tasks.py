from celery import shared_task
import logging

from django.core.mail import send_mail

logger = logging.getLogger("api")

@shared_task
def add(x, y):

    return x + y


@shared_task(bind=True, max_retries=5, default_retry_delay=10)
def scheduled_task(self):
    try:
        raise Exception(123)
        logger.info(">>> Периодическая задача выполнилась!")
    except Exception as e:
        raise self.retry()
    return True
