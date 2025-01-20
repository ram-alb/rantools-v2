from typing import List, NamedTuple, Set, TypedDict

from point_in_region import is_in_regions  # type: ignore

from bts_files.services.atoll.gsm import GsmRowFactory
from bts_files.services.atoll.lte import LteRowFactory
from bts_files.services.atoll.main import AtollData, CellRowFactory
from bts_files.services.atoll.nr import NrRowFactory
from bts_files.services.atoll.wcdma import WcdmaRowFactory


class Site(NamedTuple):
    """Represent the site data."""

    name: str
    longitude: float
    latitude: float


class SingleTechPolygon(TypedDict):
    """Represent data for cells and sites within a polygon for a single technology."""

    sites: Set[Site]
    cells: List[CellRowFactory]


class AllTechPolygon(TypedDict, total=False):
    """Represent data for cells and sites within a polygon for all technologies."""

    sites: Set[Site]
    GSM: List[GsmRowFactory]
    WCDMA: List[WcdmaRowFactory]
    LTE: List[LteRowFactory]
    NR: List[NrRowFactory]


def _filter_cells_within_polygons(
    cells: List[CellRowFactory],
    # polygons: List[GeoDataFrame],
    regions: List[str],
) -> SingleTechPolygon:
    """Filter cells that are located within the specified polygons."""
    filtered_cells = []
    filtered_sites = set()

    for cell in cells:
        # if _is_in_polygons(cell, regions):
        if is_in_regions((cell.longitude, cell.latitude), regions):
            filtered_cells.append(cell)
            filtered_sites.add(Site(
                name=cell.site,
                longitude=cell.longitude,
                latitude=cell.latitude,
            ))

    return SingleTechPolygon(
        sites=filtered_sites,
        cells=filtered_cells,
    )


def filter_cells(atoll_cells: AtollData, regions: List[str]) -> AllTechPolygon:
    """Filter cells based on their location within specified regions."""
    filtered_data: AllTechPolygon = {'sites': set()}
    for tech, cells in atoll_cells.items():
        polygons_data = _filter_cells_within_polygons(cells, regions)  # type: ignore
        filtered_data[tech] = polygons_data['cells']  # type: ignore
        filtered_data['sites'] = filtered_data['sites'].union(
            polygons_data['sites'],
        )

    return filtered_data
