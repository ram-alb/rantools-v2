from typing import NamedTuple

SELECT_ATOLL = """
    SELECT
        t.site_name,
        c.cell_id,
        ROUND(s.latitude, 5) AS latitude,
        ROUND(s.longitude, 5) AS longitude,
        t.antenna_name,
        t.height,
        t.azimut,
        t.fband,
        c.rnc_name
    FROM
        atoll_mrat.utransmitters t
        JOIN atoll_mrat.ucells c
            ON t.tx_id = c.tx_id
        JOIN atoll_mrat.sites s
            ON t.site_name = s.name
    WHERE
        t.active = -1
        AND t.site_name LIKE :site_id
    ORDER BY
        c.cell_id
"""


class AtollWcdmaCell(NamedTuple):
    """Represent a WCDMA cell in an atoll."""

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
        rncname,
        sitename,
        cell,
        localcellid,
        lac,
        ROUND(latitude, 5) as latitude,
        ROUND(longitude, 5) as longitude,
        mocncellprofile
    FROM wcdmacells2
    WHERE sitename LIKE :site_id
    ORDER BY cell
"""


class NetworkWcdmaCell(NamedTuple):
    """Represent a WCDMA cell in a network."""

    location: str
    site: str
    cell: str
    cellid: int
    lac: int
    latitude: float
    longitude: float
    sharingtype: str
