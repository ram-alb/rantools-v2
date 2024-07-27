from enum import Enum
from typing import Dict, List, Union

from bts_info.services.atoll import gsm, lte, nr, wcdma
from services.db.db import DbConnection, select

AtollData = List[Union[gsm.AtollGsmCell, wcdma.AtollWcdmaCell, lte.AtollLteCell, nr.AtolNrCell]]
NetworkData = List[
    Union[gsm.NetworkGsmCell, wcdma.NetworkWcdmaCell, lte.NetworkLteCell, nr.NetworkNrCell],
]

DbData = Dict[str, Union[AtollData, NetworkData]]


class DataSource(Enum):
    """Enumeration to represent the source of data."""

    ATOLL = 'atoll'
    NETWORK = 'network'


def select_db_data(site_id: str, source: str) -> DbData:
    """Fetch data from the database based on the provided site identifier and source."""
    sql_params = {'site_id': f'%{site_id}%'}

    atoll_sql_data = {
        'GSM': (gsm.SELECT_ATOLL, sql_params, gsm.AtollGsmCell),
        'WCDMA': (wcdma.SELECT_ATOLL, sql_params, wcdma.AtollWcdmaCell),
        'LTE': (lte.SELECT_ATOLL, sql_params, lte.AtollLteCell),
        'NR': (nr.SELECT_ATOLL, sql_params, nr.AtolNrCell),
    }

    network_sql_data = {
        'GSM': (gsm.SELECT_NETWORK, sql_params, gsm.NetworkGsmCell),
        'WCDMA': (wcdma.SELECT_NETWORK, sql_params, wcdma.NetworkWcdmaCell),
        'LTE': (lte.SELECT_NETWORK, sql_params, lte.NetworkLteCell),
        'NR': (nr.SELECT_NETWORK, sql_params, nr.NetworkNrCell),
    }

    if source == DataSource.ATOLL.value:
        sql_data = atoll_sql_data
    elif source == DataSource.NETWORK.value:
        sql_data = network_sql_data  # type: ignore
    else:
        valid_sources = ', '.join([ds.value for ds in DataSource])
        raise ValueError(f"source must be one of {valid_sources}")

    with DbConnection('oracledb') as connection:
        selected_data = {
            tech: select(connection, *sql_items)
            for tech, sql_items in sql_data.items()
        }

    if all(not row for row in selected_data.values()):
        raise RuntimeError(f"No data found for site ID: '{site_id}' with source: '{source}'.")

    return selected_data
