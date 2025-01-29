from typing import NamedTuple

atoll_nr_select = """
    SELECT
        t.site_name,
        s.lte_sitename,
        s.longitude,
        s.latitude,
        c.cell_id as cell,
        c.unique_id as cid,
        c.carrier,
        c.pci,
        c.tac,
        t.height,
        t.azimut
    FROM
        atoll_mrat.xgtransmitters t
        JOIN atoll_mrat.sites s
            ON t.site_name = s.name
        JOIN atoll_mrat.xgcells5gnr c
            ON t.tx_id = c.tx_id
    WHERE
        c.active = -1
        AND t.azimut IS NOT NULL
    ORDER BY
        c.cell_id
"""


class NrRowFactory(NamedTuple):
    """Represent a row of NR cell data."""

    site: str
    lte_sitename: str
    longitude: float
    latitude: float
    cell: str
    cid: str
    carrier: str
    pci: int
    tac: int
    height: float
    azimut: int
