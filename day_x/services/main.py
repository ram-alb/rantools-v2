from django.contrib.auth.models import Group
from send_mail import send_email

from day_x.services.reports import fill_excel
from day_x.services.sql import get_network_live_data
from network_live import update_nl


def send_dayx_file() -> None:
    """Send dayX file to emails."""
    # update Network Live data
    update_results = update_nl()

    # get updated data
    nl_data = get_network_live_data()

    # fill excell
    report_path = fill_excel(nl_data)

    # get email list of users in DayX group
    dayx_group = Group.objects.get(name='DayX')
    to = dayx_group.user_set.values_list("email", flat=True)

    # send report
    subject = 'DayX file'
    message = '\n'.join(update_results)
    send_email(list(to), subject, message, filepaths=report_path)
