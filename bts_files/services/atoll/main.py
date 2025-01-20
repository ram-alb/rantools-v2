from typing import List, TypedDict, Union

from bts_files.services.atoll.gsm import GsmRowFactory, atoll_gsm_select
from bts_files.services.atoll.lte import LteRowFactory, atoll_lte_select
from bts_files.services.atoll.nr import NrRowFactory, atoll_nr_select
from bts_files.services.atoll.wcdma import WcdmaRowFactory, atoll_wcdma_select
from services.db.db import DbConnection, select

CellRowFactory = Union[GsmRowFactory, WcdmaRowFactory, LteRowFactory, NrRowFactory]


class AtollData(TypedDict, total=False):
    """Represent a dictionary containing data for various radio access technologies."""

    GSM: List[GsmRowFactory]
    WCDMA: List[WcdmaRowFactory]
    LTE: List[LteRowFactory]
    NR: List[NrRowFactory]


def select_atoll_data(technologies: List[str]) -> AtollData:
    """Retrieve data for specified radio access technologies from the Atoll database."""
    sql_data = {
        'GSM': {'sql_select': atoll_gsm_select, 'row_factory': GsmRowFactory},
        'WCDMA': {'sql_select': atoll_wcdma_select, 'row_factory': WcdmaRowFactory},
        'LTE': {'sql_select': atoll_lte_select, 'row_factory': LteRowFactory},
        'NR': {'sql_select': atoll_nr_select, 'row_factory': NrRowFactory},
    }

    selected_data: AtollData = {}

    with DbConnection('oracledb') as connection:
        for tech in technologies:
            selected_data[tech] = select(  # type: ignore
                connection,
                **sql_data[tech],  # type: ignore
            )

    return selected_data
