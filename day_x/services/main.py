from network_live import update_nl, update_zte_gsm
from send_mail import send_email

from day_x.services.reports import fill_excel
from day_x.services.sql import get_network_live_data


def send_dayx_file() -> None:
    # update Network Live data
    # update_results = update_zte_gsm()

    # get updated data
    nl_data = get_network_live_data()

    # fill excell
    report_path = fill_excel(nl_data)

    # send report
    # to = 'Ramil.Albakov@kcell.kz'
    # subject = 'DayX file'
    # message = '\n'.join(update_results)
    # send_email(to, subject, message, filepaths=report_path)
