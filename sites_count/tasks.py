from celery import shared_task

from sites_count.services.counter.main import update_site_counts


@shared_task()
def sites_count():
    """Celery task for updating the sites count."""
    update_site_counts()
