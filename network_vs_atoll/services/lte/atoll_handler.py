import re
from typing import List, Union

from network_vs_atoll.services.lte.sql import AtollRow
from network_vs_atoll.services.utils import get_rach


def _get_earfcndl(carrier: str) -> Union[int, str]:
    if carrier is None:
        return None
    if carrier.isnumeric():
        return int(carrier)

    match = re.search(r'\((\d+)\)', carrier)
    if match:
        return int(match.group(1))

    return carrier


def handle_atoll_data(atoll_data: List[AtollRow]) -> dict:
    """Handle Atoll data and convert it to a dictionary."""
    atoll_cells = {}

    for row in atoll_data:
        earfcndl = _get_earfcndl(row.earfcndl)
        rach = get_rach(row.rach)
        try:
            cell_id = int(row.cellid)
        except TypeError:
            cell_id = row.cellid  # type: ignore

        row_params = row._asdict()
        row_params['earfcndl'] = earfcndl
        row_params['rach'] = rach
        row_params['cellid'] = cell_id
        atoll_cells[row.cell] = row_params

    return atoll_cells
