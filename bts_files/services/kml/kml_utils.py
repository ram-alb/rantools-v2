from geopy import Point  # type: ignore
from geopy.distance import geodesic  # type: ignore

from bts_files.services.atoll.main import CellRowFactory
from bts_files.services.utils import calc_azimut_beam


def get_cell_polygon_coordinates(
    cell: CellRowFactory,
    technology: str,
) -> str:
    """Get coordinates for cell polygon."""
    azimut_deltas = {
        65: 33,
        30: 15,
        360: 33,
    }

    cell_radius = {
        'GSM 900': 150,
        'GSM 1800': 120,
        'WCDMA': 90,
        'LTE': 60,
        'NR': 30,
    }

    azimut, beam_width = calc_azimut_beam(cell)

    base_point = Point(cell.latitude, cell.longitude)
    point1 = geodesic(meters=cell_radius[technology]).destination(
        base_point,
        azimut + azimut_deltas[beam_width],
    )
    point2 = geodesic(meters=cell_radius[technology]).destination(
        base_point,
        azimut - azimut_deltas[beam_width],
    )

    points = [base_point, point1, point2, base_point]
    coordinates = [
        f'{point.longitude},{point.latitude},0 ' for point in points
    ]

    return ''.join(coordinates)
