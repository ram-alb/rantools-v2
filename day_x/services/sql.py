from typing import Dict, List

from services.db.db import DbConnection, select

GSM_SELECT = """
SELECT
    SITENAME,
    BSCID,
    LAC,
    CELLID,
    CELL,
    LONGITUDE,
    LATITUDE,
    'gsm' as TECHNOLOGY,
    CONCAT(NCC, BCC) as BSIC,
    BSCNAME
FROM
    GSMCELLS2
"""

WCDMA_SELECT = """
SELECT
    SITENAME,
    RNCID,
    LAC,
    CID,
    CELL,
    LONGITUDE,
    LATITUDE,
    'umts' as TECHNOLOGY,
    PSC,
    RNCNAME
FROM
    WCDMACELLS2
"""

LTE_SELECT = """
SELECT
    SITENAME,
    NODEID,
    TAC,
    CELL,
    LONGITUDE,
    LATITUDE,
    'lte' as TECHNOLOGY,
    NODEID,
    CELLID,
    PHYSICALCELLID,
    SUBNETWORK
FROM
    LTECELLS2
"""


def get_network_live_data() -> Dict[str, List[tuple]]:
    """Get network live cell data."""
    selects = {
        'GSM': GSM_SELECT,
        'WCDMA': WCDMA_SELECT,
        'LTE': LTE_SELECT,
    }

    with DbConnection('oracledb') as connection:
        network_live_data = {
            tech: select(connection, sql) for tech, sql in selects.items()
        }

    return network_live_data
