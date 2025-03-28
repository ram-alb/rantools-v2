from typing import List, Tuple

from services.db.db import DbConnection, select


def select_tr_data() -> Tuple[List[str], List[tuple]]:
    """Select all data from the SITE_TR_DATA table."""
    columns_query = """
        SELECT COLUMN_NAME
        FROM ALL_TAB_COLUMNS
        WHERE TABLE_NAME = 'SITE_TR_DATA'
        ORDER BY COLUMN_ID
    """
    data_query = "SELECT * FROM SITE_TR_DATA"

    with DbConnection("oracledb") as connection:
        columns = select(connection, columns_query)
        columns_list = [column[0] for column in columns]

        tr_data = select(connection, data_query)

        return columns_list, tr_data
