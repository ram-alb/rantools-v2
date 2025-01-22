from collections import namedtuple
from datetime import date
from typing import List

from services.db.db import DbConnection, select


def select_by_operators(requested_date: date) -> List:
    """Select site count data counted by operators."""
    sql_command = """
        SELECT * FROM sites_by_operators
        WHERE created_at = :requested_date
    """

    sql_params = {'requested_date': requested_date}

    row_factory = namedtuple('SitesByOperators', [
        'created_at',
        'total',
        'gsm',
        'wcdma',
        'lte',
        'nr5g',
        'iot',
        'kcell_total',
        'kcell_gsm',
        'kcell_wcdma',
        'kcell_lte',
        'kcell_nr5g',
        'kcell_iot',
        'tele2_total',
        'tele2_gsm',
        'tele2_wcdma',
        'tele2_lte',
        'tele2_nr5g',
        'beeline_total',
        'beeline_gsm',
        'beeline_wcdma',
        'beeline_lte',
        'beeline_nr5g',
    ])

    with DbConnection('oracledb') as connection:
        return select(connection, sql_command, sql_params, row_factory)
