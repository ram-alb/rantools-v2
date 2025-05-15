from typing import NamedTuple

NETWORK_QUERY = r"""
SELECT
    subnetwork,
    sitename,
    cell,
    cellid,
    nrpci,
    nrtac,
    rachrootsequence,
    arfcndl,
    bschannelbwdl
FROM nrcells
WHERE oss LIKE 'ENM%'
    AND REGEXP_LIKE(cell, '^\d{5}')
"""

ATOLL_QUERY = """
SELECT
    t.site_name,
    c.cell_id,
    c.unique_id,
    c.pci,
    c.tac,
    c.prach_rsi_list,
    c.carrier
FROM atoll_mrat.xgcells5gnr c
    LEFT JOIN atoll_mrat.xgtransmitters t
        ON c.tx_id = t.tx_id
WHERE c.active = -1
"""


class NetworkRow(NamedTuple):
    """Network row from the database."""

    subnetwork: str
    site: str
    cell: str
    cellid: int
    nrpci: int
    nrtac: int
    rach: int
    arfcndl: int
    bandwidth: int


class AtollRow(NamedTuple):
    """Atoll row from the database."""

    site: str
    cell: str
    cellid: str
    nrpci: int
    nrtac: int
    rach: str
    carrier: str
