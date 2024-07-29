from typing import Any, Dict, List, Tuple

from bts_info.services.atoll.main import select_db_data
from bts_info.services.enm.main import get_mimo_order
from bts_info.services.handler import append_mimo_order
from bts_info.services.sector_polygons import Polygons, make_sector_polygons

SiteData = Tuple[
    List[Dict[str, Any]],
    Polygons,
    float,
    float,
]


def get_site_data(site_id: str, source: str) -> SiteData:
    """Fetch site data from the database, retrieves MIMO orders, and generates sector polygons."""
    db_data = select_db_data(site_id, source)
    mimo_orders = get_mimo_order(site_id)
    sites = append_mimo_order(db_data, mimo_orders)

    polygons = []
    for tech, selected_data in db_data.items():
        if source == 'atoll':
            polygons += make_sector_polygons(selected_data, tech)  # type: ignore

    try:
        lat, lon = polygons[0]['point0']  # type: ignore
    except IndexError:
        lat, lon = (None, None)

    return sites, polygons, lat, lon  # type: ignore
