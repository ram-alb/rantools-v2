from celery import shared_task

from config.redis import acquire_lock, release_lock
from day_x.services.main import send_dayx_file

DAYX_FILE_LOCK_KEY = 'dayx_file_task_lock'


@shared_task()
def update_dayx_file():
    """Celery task for updating and sending the DayX file."""
    lock_timeout = 1800

    if not acquire_lock(DAYX_FILE_LOCK_KEY, lock_timeout):
        return
    try:
        send_dayx_file()
    finally:
        release_lock(DAYX_FILE_LOCK_KEY)
