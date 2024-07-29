from typing import NamedTuple

atoll_wcdma_select = """
    SELECT
        c.rnc_name,
        t.site_name,
        s.longitude,
        s.latitude,
        c.cell_id as cell,
        c.carrier,
        c.cell_identity as cid,
        c.scrambling_code as psc,
        c.lac,
        t.height,
        t.azimut
    FROM
        atoll_mrat.utransmitters t
        JOIN atoll_mrat.sites s
            ON t.site_name = s.name
        JOIN atoll_mrat.ucells c
            ON t.tx_id = c.tx_id
    WHERE
        t.active = -1
        AND c.carrier IN (10562, 10587)
        AND t.azimut IS NOT NULL
    ORDER BY
        c.cell_id
"""


class WcdmaRowFactory(NamedTuple):
    """Represent a row of WCDMA cell data."""

    rnc: str
    site: str
    longitude: float
    latitude: float
    cell: str
    carrier: int
    cid: int
    psc: int
    lac: int
    height: float
    azimut: int
