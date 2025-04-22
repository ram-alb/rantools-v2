from typing import NamedTuple

NETWORK_QUERY = r"""
SELECT
    subnetwork,
    sitename,
    cell,
    tac,
    cellid,
    physicalcellid,
    earfcndl,
    rachrootsequence
FROM network_live.ltecells2
WHERE oss LIKE 'ENM%'
    AND REGEXP_LIKE(cell, '^\d{5}')
"""


ATOLL_QUERY = r"""
SELECT
    s.name as site,
    c.cell_id as cell,
    c.tac,
    c.unique_id as cellid,
    c.pci,
    c.carrier,
    c.prach_rsi_list as rach_list
FROM atoll_mrat.xgcellslte c
    LEFT JOIN atoll_mrat.xgtransmitters t
        ON c.tx_id = t.tx_id
    LEFT JOIN atoll_mrat.sites s
        ON t.site_name = s.name
WHERE c.active = -1
    AND REGEXP_LIKE (c.cell_id, '^\d{5}')
"""


class NetworkRow(NamedTuple):
    """Network row from the database."""

    subnetwork: str
    site: str
    cell: str
    tac: int
    cellid: int
    pci: int
    earfcndl: int
    rach: int


class AtollRow(NamedTuple):
    """Atoll row from the database."""

    site: str
    cell: str
    tac: int
    cellid: str
    pci: int
    earfcndl: str
    rach: str
