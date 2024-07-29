from typing import List, NamedTuple, Set, TypedDict

import geopandas as gpd  # type: ignore
from geopandas import GeoDataFrame
from shapely.geometry import Point  # type: ignore

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


def _is_in_polygons(cell: CellRowFactory, polygons: List[GeoDataFrame]) -> bool:
    """Check if a given cell is within any of the provided polygons."""
    cell_point = Point(cell.longitude, cell.latitude)
    cell_within_polygons = [
        cell_point.within(polygon) for polygon in polygons
    ]
    return any(cell_within_polygons)


def _get_polygons(regions: List[str]) -> List[GeoDataFrame]:
    """Get polygons for the requested regions."""
    map_paths = {
        'Astana-city': 'maps/astana-city/astana-city.shp',
        'Akmola-obl': 'maps/akmola-obl/akmola-obl.shp',
        'Almaty-city': 'maps/almaty-city/almaty-city.shp',
        'Almaty-obl': 'maps/almaty-obl/almaty-obl.shp',
        'Aktobe-region': 'maps/aktobe-obl/aktobe-obl.shp',
        'Atyrau-region': 'maps/atyrau-obl/atyrau-obl.shp',
        'Karaganda-region': 'maps/karaganda-obl/karaganda-obl.shp',
        'Kostanay-region': 'maps/kostanay-obl/kostanay-obl.shp',
        'Kyzylorda-region': 'maps/kyzylorda-obl/kyzylorda-obl.shp',
        'Mangystau-region': 'maps/mangystau-obl/mangystau-obl-polygon.shp',
        'Pavlodar-region': 'maps/pavlodar-obl/pavlodar-obl.shp',
        'North-Kazakhstan': 'maps/sko/sko.shp',
        'South-Kazakhstan': 'maps/uko/uko.shp',
        'East-Kazakhstan': 'maps/vko/vko.shp',
        'Zhambyl-region': 'maps/zhambyl-obl/zhambyl-obl.shp',
        'West-Kazakhstan': 'maps/zko/zko-polygon.shp',
        'Kazmin': 'maps/kazmin/Kazmin-polygon.shp',
    }

    polygons = []
    for region in regions:
        if region == 'Almaty-region':
            polygon_city = gpd.read_file(map_paths['Almaty-city'])
            polygons.append(polygon_city.geometry[0])
            polygon_region = gpd.read_file(map_paths['Almaty-obl'])
            polygons.append(polygon_region.geometry[0])
        elif region == 'Astana-region':
            polygon_city = gpd.read_file(map_paths['Astana-city'])
            polygons.append(polygon_city.geometry[0])
            polygon_region = gpd.read_file(map_paths['Akmola-obl'])
            polygons.append(polygon_region.geometry[0])
        else:
            polygon_data = gpd.read_file(map_paths[region])
            polygons.append(polygon_data.geometry[0])

    return polygons


def _filter_cells_within_polygons(
    cells: List[CellRowFactory],
    polygons: List[GeoDataFrame],
) -> SingleTechPolygon:
    """Filter cells that are located within the specified polygons."""
    filtered_cells = []
    filtered_sites = set()

    for cell in cells:
        if _is_in_polygons(cell, polygons):
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
    polygons = _get_polygons(regions)

    filtered_data: AllTechPolygon = {'sites': set()}
    for tech, cells in atoll_cells.items():
        polygons_data = _filter_cells_within_polygons(cells, polygons)  # type: ignore
        filtered_data[tech] = polygons_data['cells']  # type: ignore
        filtered_data['sites'] = filtered_data['sites'].union(
            polygons_data['sites'],
        )

    return filtered_data
