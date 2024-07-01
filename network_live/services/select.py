"""Select cell data from network_live."""

from typing import Dict, List, Tuple

from services.db.connector import DBConnector
from services.db.network_live import Tables

InnerTuple = Tuple[List[Tuple], List[str]]


def select_data(technologies: List[str]) -> Dict[str, InnerTuple]:
    """Select cell data from network_live."""
    network_live_tables = {table.name.split('_')[0]: table.value for table in Tables}
    network_live_data = {}

    with DBConnector.get_connection() as connection:
        cursor = connection.cursor()
        for technology in technologies:
            column_query = """
                SELECT COLUMN_NAME
                FROM ALL_TAB_COLUMNS
                WHERE TABLE_NAME = :table_name
                ORDER BY COLUMN_ID
            """
            cursor.execute(column_query, table_name=(network_live_tables[technology]).upper())
            columns = cursor.fetchall()
            column_list = [column[0] for column in columns]

            data_query = 'SELECT * FROM {table}'.format(table=network_live_tables[technology])
            cursor.execute(data_query)
            cell_data = cursor.fetchall()

            network_live_data[technology] = (cell_data, column_list)

    return network_live_data
