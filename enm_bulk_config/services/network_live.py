import pandas as pd

from services.db.db import DbConnection, select
from services.db.network_live import Tables


def get_network_live_df(technology: str) -> pd.DataFrame:
    """Get network live data for the specified technology and parameter."""
    try:
        table_name = Tables.get_table(technology).value
    except ValueError as err:
        raise ValueError(f"Invalid technology '{technology}': {err}")

    sql_select = f"""
    SELECT
        sitename,
        cell,
        oss
    FROM {table_name}
    WHERE oss LIKE 'ENM%'
    """

    with DbConnection(db_type="oracledb") as connection:
        rows = select(connection, sql_select)
        df = pd.DataFrame(rows, columns=["sitename", "cell", "enm"])

    return df
