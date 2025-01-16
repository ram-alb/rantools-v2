"""Select cell data from network_live."""

from typing import Dict, List, Tuple

from services.db.db import DbConnection, select
from services.db.network_live import Tables

COLUMN_QUERY = """
    SELECT COLUMN_NAME
    FROM ALL_TAB_COLUMNS
    WHERE TABLE_NAME = :table_name
    ORDER BY COLUMN_ID
"""

Technology = str
Headers = List[str]
Rows = List[tuple]
DbData = Tuple[Rows, Headers]
NetworkLiveData = Dict[Technology, DbData]


def select_data(technologies: List[str]) -> NetworkLiveData:
    """Select cell data from network_live."""
    network_live_tables = {table.name.split('_')[0]: table.value for table in Tables}
    network_live_data = {}

    with DbConnection('oracledb') as connection:
        for technology in technologies:
            table_name = network_live_tables[technology].upper()
            columns = select(connection, COLUMN_QUERY, {'table_name': table_name})
            column_list = [column[0] for column in columns]

            data_query = 'SELECT * FROM {table}'.format(table=network_live_tables[technology])
            cell_data = select(connection, data_query)

            network_live_data[technology] = (cell_data, column_list)

    return network_live_data
