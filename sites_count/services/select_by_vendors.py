from collections import namedtuple
from datetime import date
from typing import List

from services.db.db import DbConnection, select


def select_by_vendors(requested_date: date) -> List:
    """Select site count data counted by vendors."""
    sql_command = """
        SELECT * FROM sites_by_vendors
        WHERE created_at = :requested_date
    """

    sql_params = {'requested_date': requested_date}

    row_factory = namedtuple('SitesByVendors', [
        'created_at',
        'ericsson_total',
        'ericsson_gsm',
        'ericsson_wcdma',
        'ericsson_lte',
        'ericsson_nr5g',
        'ericsson_iot',
        'zte_total',
        'zte_gsm',
        'zte_wcdma',
        'huawei_total',
        'huawei_gsm',
        'huawei_wcdma',
        'huawei_lte',
        'huawei_nr5g',
        'nokia_total',
        'nokia_gsm',
        'nokia_wcdma',
        'nokia_lte',
        'nokia_nr5g',
    ])

    with DbConnection('oracledb') as connection:
        return select(connection, sql_command, sql_params, row_factory)
