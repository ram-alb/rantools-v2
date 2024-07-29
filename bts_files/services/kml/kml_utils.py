from geopy import Point  # type: ignore
from geopy.distance import geodesic  # type: ignore

from bts_files.services.atoll.main import CellRowFactory


def get_cell_polygon_coordinates(
    cell: CellRowFactory,
    technology: str,
    antenna_type: str = 'single_beam',
) -> str:
    """Get coordinates for cell polygon."""
    azimut_deltas = {
        'single_beam': 33,
        'dual_beam': 16,
    }

    cell_radius = {
        'GSM 900': 150,
        'GSM 1800': 120,
        'WCDMA': 90,
        'LTE': 60,
        'NR': 30,
    }

    base_point = Point(cell.latitude, cell.longitude)
    point1 = geodesic(meters=cell_radius[technology]).destination(
        base_point,
        cell.azimut + azimut_deltas[antenna_type],
    )
    point2 = geodesic(meters=cell_radius[technology]).destination(
        base_point,
        cell.azimut - azimut_deltas[antenna_type],
    )

    points = [base_point, point1, point2, base_point]
    coordinates = [
        f'{point.longitude},{point.latitude},0 ' for point in points
    ]

    return ''.join(coordinates)
