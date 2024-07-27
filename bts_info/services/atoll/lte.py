from typing import NamedTuple

SELECT_ATOLL = """
    SELECT
        COALESCE(s.name, s.lte_sitename) AS site_name,
        c.cell_id,
        ROUND(s.latitude, 5) AS latitude,
        ROUND(s.longitude, 5) AS longitude,
        t.antenna_name,
        t.height,
        t.azimut,
        t.fband,
        s.lte_region
    FROM
        atoll_mrat.sites s
    INNER JOIN
        atoll_mrat.xgtransmitters t
        ON s.name = t.site_name
    INNER JOIN
        atoll_mrat.xgcellslte c
        ON t.tx_id = c.tx_id
    WHERE
        t.active = -1
        AND (s.lte_sitename LIKE :site_id OR s.name LIKE :site_id)
    ORDER BY
        site_name, c.cell_id
"""


class AtollLteCell(NamedTuple):
    """Represent a LTE cell in an atoll."""

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
        subnetwork,
        sitename,
        eutrancell,
        cellid,
        tac
    FROM ltecells2
    WHERE sitename LIKE :site_id
    ORDER BY cellid
"""


class NetworkLteCell(NamedTuple):
    """Represent a LTE cell in a network."""

    location: str
    site: str
    cell: str
    cellid: int
    tac: int
