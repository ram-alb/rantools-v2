import re
from typing import List

from network_vs_atoll.services.lte.sql import AtollRow
from network_vs_atoll.services.utils import AtollParams, ParameterValue, get_rach, handle_cellid


def _get_earfcndl(carrier: str) -> ParameterValue:
    if carrier is None:
        return None
    if carrier.isnumeric():
        return int(carrier)

    match = re.search(r'\((\d+)\)', carrier)
    if match:
        return int(match.group(1))

    return carrier


def handle_atoll_data(atoll_data: List[AtollRow]) -> AtollParams:
    """Handle Atoll data and convert it to a dictionary."""
    atoll_cells = {}

    for row in atoll_data:
        row_params = row._asdict()

        earfcndl = _get_earfcndl(row.earfcndl)
        row_params['earfcndl'] = earfcndl

        rach = get_rach(row.rach)
        row_params['rach'] = rach

        cell_id = handle_cellid(row.cellid)
        row_params['cellid'] = cell_id

        atoll_cells[row.cell] = row_params

    return atoll_cells
