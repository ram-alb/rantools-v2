from typing import Optional, Tuple

from bts_files.services.atoll.main import CellRowFactory

DEFAULT_WIDTH = 65


def _get_branch(cell: str) -> Optional[str]:
    dual_beam_markers = ['D2L', 'D2R', 'D4L', 'D4R']

    for marker in dual_beam_markers:
        if marker in cell:
            return cell[-1]

    site_id = cell[:5]
    branch = cell[-1]
    if site_id.isnumeric() and branch in {'L', 'R'}:
        return branch

    return None


def calc_azimut_beam(cell: CellRowFactory) -> Tuple[int, int]:
    """Calculate the azimuth and beam width for the cell."""
    dual_beam_delta = 17
    dual_beam_width = 30
    dot_beam_width = 360
    max_azimut = 360

    branch = _get_branch(cell.cell)

    if branch == 'L':
        azimut = (cell.azimut - dual_beam_delta) % max_azimut
        return azimut, dual_beam_width
    elif branch == 'R':
        azimut = (cell.azimut + dual_beam_delta) % max_azimut
        return azimut, dual_beam_width
    elif cell.cell.endswith('DOT'):
        azimut = 0
        return azimut, dot_beam_width

    return cell.azimut, DEFAULT_WIDTH
