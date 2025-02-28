from typing import Tuple

from services.db.db import DbConnection

SQL_SELECT = """
SELECT *
FROM HW_INFO
WHERE nodename LIKE :query
"""


def get_site_hw(query: str) -> Tuple[list, list]:
    """Get site hardware data from the database."""
    query = f'%{query}%'
    with DbConnection('oracledb') as connection:
        cursor = connection.cursor()
        cursor.execute(SQL_SELECT, {'query': query})

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        sorted_rows = sorted(rows, key=lambda entry: entry[5])

        return columns, sorted_rows
