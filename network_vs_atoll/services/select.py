from typing import Any, List

from services.db.db import DbConnection, select


def select_db_data(sql_query: str, row_factory: Any = None) -> List[Any]:
    """Select data from the database."""
    with DbConnection('oracledb') as connection:
        selected_data = select(
            connection,
            sql_select=sql_query,
            row_factory=row_factory,
        )
    return selected_data
