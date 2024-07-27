from typing import Dict, List, Tuple, Union

from geopy.distance import geodesic  # type: ignore

from bts_info.services.atoll.main import AtollData

Polygons = List[Dict[str, Union[str, Tuple[float, float]]]]


def make_sector_polygons(selected_data: AtollData, technology: str) -> Polygons:
    """Generate sector polygons for a given technology based on the provided data."""
    dist = {
        'GSM': 0.4,
        'WCDMA': 0.3,
        'LTE': 0.2,
        'NR': 0.1,
    }

    colors = {
        'GSM': 'green',
        'WCDMA': 'red',
        'LTE': 'yellow',
        'NR': 'blue',
    }

    sector_points = []
    azimut_delta_left = -30
    azimut_delta_right = 30

    for row in selected_data:
        base_point = (row.latitude, row.longitude)
        point1 = geodesic(kilometers=dist[technology]).destination(
            base_point,
            bearing=row.azimut + azimut_delta_left,
        )
        point2 = geodesic(kilometers=dist[technology]).destination(
            base_point,
            bearing=row.azimut + azimut_delta_right,
        )
        sector_points.append(
            {
                'point0': base_point,
                'point1': (point1.latitude, point1.longitude),
                'point2': (point2.latitude, point2.longitude),
                'color': colors[technology],
            },
        )

    return sector_points  # type: ignore
