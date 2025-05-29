from typing import Dict, List

import pandas as pd

from services.db.db import DbConnection, select
from services.db.network_live import Tables

param_map = {
    "LTE": {
        "PCI": "PHYSICALCELLID",
        "RACH": "RACHROOTSEQUENCE",
        "TAC": "TAC",
        "CellId": "CELLID",
    },
    "NR": {
        "PCI": "NRPCI",
        "RACH": "RACHROOTSEQUENCE",
        "TAC": "NRTAC",
        "CellId": "CELLID",
    },
}


def get_all_params() -> Dict[str, List[str]]:
    """Get all parameters for each technology."""
    return {tech: list(tech_params.keys()) for tech, tech_params in param_map.items()}


def _get_parameter_column(technology: str, parameter: str) -> str:
    """Get the database column name for the specified technology and parameter."""
    if technology not in param_map:
        raise ValueError(f"Invalid technology '{technology}'.")

    tech_params = param_map[technology]
    if parameter not in tech_params:
        raise ValueError(
            f"Invalid parameter '{parameter}' for technology '{technology}'.",
        )

    return tech_params[parameter]


def get_network_live_df(technology: str, parameter: str) -> pd.DataFrame:
    """Get network live data for the specified technology and parameter."""
    try:
        table_name = Tables.get_table(technology).value
    except ValueError as err:
        raise ValueError(f"Invalid technology '{technology}': {err}")

    param_column = _get_parameter_column(technology, parameter)

    sql_select = f"""
    SELECT
        sitename,
        cell,
        {param_column}
    FROM {table_name}
    WHERE oss LIKE 'ENM%'
    """

    with DbConnection(db_type="oracledb") as connection:
        rows = select(connection, sql_select)
        df = pd.DataFrame(rows, columns=["sitename", "cell", param_column])

    return df
