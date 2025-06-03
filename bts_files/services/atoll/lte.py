from typing import NamedTuple

atoll_lte_select = """
    SELECT
        s.lte_region,
        t.site_name,
        s.lte_sitename,
        s.longitude,
        s.latitude,
        c.cell_id as cell,
        c.carrier,
        c.unique_id as cid,
        c.pci,
        c.prach_rsi_list,
        c.tac,
        t.height,
        t.azimut,
        t.antenna_name
    FROM
        atoll_mrat.xgtransmitters t
        JOIN atoll_mrat.sites s
            ON t.site_name = s.name
        JOIN atoll_mrat.xgcellslte c
            ON t.tx_id = c.tx_id
    WHERE
        t.active = -1
        AND t.azimut IS NOT NULL
    ORDER BY
        c.cell_id
"""


class LteRowFactory(NamedTuple):
    """Represent a row of LTE cell data."""

    subnetwork: str
    site: str
    lte_sitename: str
    longitude: float
    latitude: float
    cell: str
    carrier: str
    cid: str
    pci: int
    prach: str
    tac: int
    height: float
    azimut: int
    antenna: str
