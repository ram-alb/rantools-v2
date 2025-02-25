from typing import Dict, List

from services.db.db import DbConnection, select

GSM_SELECT = """
SELECT DISTINCT
    operator,
    sitename,
    vendor,
    region
FROM GSMCELLS2
WHERE sitename IS NOT NULL
"""

WCDMA_SELECT = """
SELECT DISTINCT
    operator,
    sitename,
    vendor,
    region
FROM WCDMACELLS2
WHERE sitename IS NOT NULL
"""

LTE_SELECT = """
SELECT DISTINCT
    CASE
        WHEN subnetwork NOT IN ('Tele2', 'Beeline') THEN 'Kcell'
        ELSE subnetwork
    END AS operator,
    sitename,
    vendor,
    region
FROM LTECELLS2
WHERE sitename IS NOT NULL
"""

NR_SELECT = """
SELECT DISTINCT
    CASE
        WHEN subnetwork NOT IN ('Tele2', 'Beeline') THEN 'Kcell'
        ELSE subnetwork
    END AS operator,
    sitename,
    vendor,
    region
FROM NRCELLS
WHERE sitename IS NOT NULL
"""

IOT_SELECT = """
SELECT DISTINCT
    CASE
        WHEN subnetwork NOT IN ('Tele2', 'Beeline') THEN 'Kcell'
        ELSE subnetwork
    END AS operator,
    sitename,
    vendor,
    region
FROM IOTCELLS
WHERE sitename IS NOT NULL
"""

sql_selects = {
    'GSM': GSM_SELECT,
    'WCDMA': WCDMA_SELECT,
    'LTE': LTE_SELECT,
    'NR': NR_SELECT,
    'IoT': IOT_SELECT,
}


def select_from_network_live() -> Dict[str, List[tuple]]:
    """Select data from the network live tables."""
    nl_data = {}
    with DbConnection('oracledb') as connection:
        nl_data = {
            tech: select(connection, sql_query)
            for tech, sql_query in sql_selects.items()
        }
    return nl_data
