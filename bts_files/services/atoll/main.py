from typing import List, NamedTuple, TypedDict, Union

from bts_files.services.atoll.gsm import GsmRowFactory, atoll_gsm_select
from bts_files.services.atoll.lte import LteRowFactory, atoll_lte_select
from bts_files.services.atoll.nr import NrRowFactory, atoll_nr_select
from bts_files.services.atoll.wcdma import WcdmaRowFactory, atoll_wcdma_select
from services.db.connector import Connection, DBConnector

CellRowFactory = Union[GsmRowFactory, WcdmaRowFactory, LteRowFactory, NrRowFactory]


class AtollData(TypedDict, total=False):
    """Represent a dictionary containing data for various radio access technologies."""

    GSM: GsmRowFactory
    WCDMA: WcdmaRowFactory
    LTE: LteRowFactory
    NR: NrRowFactory


def _select(
    connection: Connection,
    sql_select: str,
    row_factory: CellRowFactory,
) -> List[NamedTuple]:
    """Execute a SELECT SQL query and returns the result as a list of named tuples."""
    with connection.cursor() as cursor:
        cursor.execute(sql_select)
        cursor.rowfactory = row_factory
        selected_data = cursor.fetchall()

    connection.close()
    return selected_data


def select_atoll_data(technologies: List[str]) -> AtollData:
    """Retrieve data for specified radio access technologies from the Atoll database."""
    sql_data = {
        'GSM': (atoll_gsm_select, GsmRowFactory),
        'WCDMA': (atoll_wcdma_select, WcdmaRowFactory),
        'LTE': (atoll_lte_select, LteRowFactory),
        'NR': (atoll_nr_select, NrRowFactory),
    }

    selected_data: AtollData = {}

    for tech in technologies:
        selected_data[tech] = _select(  # type: ignore
            DBConnector.get_connection('atoll_oracledb'),
            *sql_data[tech],  # type: ignore
        )

    return selected_data
