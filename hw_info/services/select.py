from typing import Tuple

from services.db.db import DbConnection, select


def select_hw_data() -> Tuple[list, list]:
    """Select all data from the HW_INFO table."""
    columns_query = """
        SELECT COLUMN_NAME
        FROM ALL_TAB_COLUMNS
        WHERE TABLE_NAME = 'HW_INFO'
        ORDER BY COLUMN_ID
    """
    data_query = "SELECT * FROM HW_INFO"

    with DbConnection('oracledb') as connection:
        columns = select(connection, columns_query)
        columns_list = [column[0] for column in columns]

        tr_data = select(connection, data_query)

        return columns_list, tr_data
