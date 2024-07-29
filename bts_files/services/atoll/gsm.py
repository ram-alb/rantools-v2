from typing import NamedTuple

atoll_gsm_select = """
    SELECT
        g.bsc,
        g.site_name,
        s.longitude,
        s.latitude,
        g.tx_id as cell,
        g.cell_identity as cid,
        g.control_channel,
        g.bsic,
        g.lac,
        g.height,
        g.azimut,
        g.fband
    FROM
        atoll_mrat.gtransmitters g
        JOIN atoll_mrat.sites s
            ON g.site_name = s.name
    WHERE
        g.active = -1
        AND g.azimut IS NOT NULL
    ORDER BY
        g.tx_id
"""


class GsmRowFactory(NamedTuple):
    """Represent a row of GSM cell data."""

    bsc: str
    site: str
    longitude: float
    latitude: float
    cell: str
    cid: int
    bcch: int
    bsic: str
    lac: str
    height: float
    azimut: int
    fband: str
