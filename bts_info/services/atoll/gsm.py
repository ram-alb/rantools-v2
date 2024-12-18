from typing import NamedTuple

SELECT_ATOLL = """
    SELECT
        t.site_name,
        t.tx_id,
        ROUND(s.latitude, 5) AS latitude,
        ROUND(s.longitude, 5) AS longitude,
        t.antenna_name,
        t.height,
        t.azimut,
        t.fband,
        s.bsc_name
    FROM
        atoll_mrat.gtransmitters t
        JOIN atoll_mrat.sites s
            ON t.site_name = s.name
    WHERE
        t.active = -1
        AND t.site_name LIKE :site_id
    ORDER BY
        t.tx_id
"""


class AtollGsmCell(NamedTuple):
    """Represent a GSM cell in an atoll."""

    site: str
    cell: str
    latitude: float
    longitude: float
    antenna_type: str
    height: float
    azimut: int
    band: str
    location: str


SELECT_NETWORK = """
    SELECT
        bscname,
        sitename,
        cell,
        cellid,
        lac,
        ROUND(latitude, 5) as latitude,
        ROUND(longitude, 5) as longitude
    FROM gsmcells2
    WHERE sitename LIKE :site_id
    ORDER BY cell
"""


class NetworkGsmCell(NamedTuple):
    """Represent a GSM cell in a network."""

    location: str
    site: str
    cell: str
    cellid: int
    lac: int
    latitude: float
    longitude: float
