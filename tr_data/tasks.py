from celery import shared_task

from tr_data.services.db import update_sts_data
from tr_data.services.enm import get_enm_sts_data


@shared_task()
def update_sts():
    """Celery task for updating synchronization statuses."""
    enm_sts_data = get_enm_sts_data()
    update_sts_data(enm_sts_data)
