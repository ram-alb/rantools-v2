import re
from typing import List, Optional, Tuple

from network_vs_atoll.services.nr.sql import AtollRow
from network_vs_atoll.services.utils import AtollParams, get_rach, handle_cellid


def _extract_bandwidth_arfcndl(carrier: str) -> Tuple[Optional[int], Optional[int]]:
    pattern = re.compile(r'(?P<bandwidth>\d+)\s*MHz.*?(?:[^0-9]|^)(?P<frequency>\d+)(?:\)|$)')
    match = pattern.search(carrier)
    if match:
        bandwidth = int(match.group('bandwidth'))
        arfcndl = int(match.group('frequency'))
        return bandwidth, arfcndl
    return None, None


def handle_atoll_data(atoll_data: List[AtollRow]) -> AtollParams:
    """Handle Atoll data and convert it to a dictionary."""
    atoll_cells: AtollParams = {}

    for row in atoll_data:
        row_params = row._asdict()

        cell_id = handle_cellid(row.cellid)
        row_params['cellid'] = cell_id

        rach = get_rach(row.rach)
        row_params['rach'] = rach

        bandwidth, arfcndl = _extract_bandwidth_arfcndl(row_params.pop('carrier', ''))
        row_params['bandwidth'] = bandwidth
        row_params['arfcndl'] = arfcndl

        atoll_cells[row.cell] = row_params

    return atoll_cells
