import itertools
from typing import List, Set, Tuple, Union

from bts_files.services.atoll.gsm import GsmRowFactory
from bts_files.services.atoll.lte import LteRowFactory
from bts_files.services.atoll.main import CellRowFactory
from bts_files.services.atoll.nr import NrRowFactory
from bts_files.services.atoll.wcdma import WcdmaRowFactory
from bts_files.services.filter_cells import Site
from bts_files.services.kml.kml_utils import get_cell_polygon_coordinates
from bts_files.services.kml.template import render_template


def _get_gsm_kml_data(cell: GsmRowFactory) -> Tuple[str, str, str]:
    description = render_template('gsm_description.kml', {'cell': cell})

    if cell.fband == 'GSM 1800':
        style = '#msn_ylw-pushpin'
    else:
        style = '#msn_ylw-pushpin0'

    polygon_coordinates = get_cell_polygon_coordinates(cell, cell.fband)

    return (description, style, polygon_coordinates)


def _get_wcdma_kml_data(cell: WcdmaRowFactory) -> Tuple[str, str, str]:
    description = render_template('wcdma_description.kml', {'cell': cell})
    style = '#msn_ylw-pushpin3'
    polygon_coordinates = get_cell_polygon_coordinates(cell, 'WCDMA')

    return (description, style, polygon_coordinates)


def _get_lte_kml_data(cell: LteRowFactory) -> Tuple[str, str, str]:
    description = render_template('lte_description.kml', {'cell': cell})
    style = '#msn_ylw-pushpin1'
    polygon_coordinates = get_cell_polygon_coordinates(cell, 'LTE')

    return (description, style, polygon_coordinates)


def _get_nr_kml_data(cell: NrRowFactory) -> Tuple[str, str, str]:
    description = render_template('nr_description.kml', {'cell': cell})
    style = '#msn_ylw-pushpin2'
    polygon_coordinates = get_cell_polygon_coordinates(cell, 'NR')

    return (description, style, polygon_coordinates)


def _make_cell_placemark(cell: CellRowFactory, technology: str) -> str:
    cell_utils = {
        'GSM': _get_gsm_kml_data,
        'WCDMA': _get_wcdma_kml_data,
        'LTE': _get_lte_kml_data,
        'NR': _get_nr_kml_data,
    }
    description, style, polygon_coordinates = cell_utils[technology](cell)  # type: ignore
    return render_template(
        'cell_placemark.kml',
        {
            'cell': cell,
            'description': description,
            'style': style,
            'polygon_coordinates': polygon_coordinates,
        },
    )


def make_kml_folder(placemark_data: Union[List[CellRowFactory], Set[Site]], technology: str) -> str:
    """Generate a KML folder containing placemarks for the given technology."""
    kml_data = [f'<Folder>\n<name>{technology}</name>\n<open>1</open>']
    for placemark_item in placemark_data:
        if technology == 'sites':
            placemark = render_template('site_placemark.kml', {'site': placemark_item})
        else:
            placemark = _make_cell_placemark(placemark_item, technology)  # type: ignore
        kml_data.append(placemark)

    kml_folder = itertools.chain(kml_data, ['\n</Folder>'])
    return '\n'.join(kml_folder)
