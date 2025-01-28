from typing import Tuple

from bts_files.services.atoll.lte import LteRowFactory

DEFAULT_WIDTH = 65


def calc_azimut_beam(cell: LteRowFactory) -> Tuple[int, int]:
    """Calculate the azimuth and beam width for the cell."""
    dual_beam_markers = ['D2L', 'D2R', 'D4L', 'D4R']
    dual_beam_delta = 17
    dual_beam_width = 30
    dot_beam_width = 360
    max_azimut = 360

    branch = None
    for marker in dual_beam_markers:
        if marker in cell.cell:
            branch = cell.cell[-1]
            break

    if branch == 'L':
        azimut = (cell.azimut - dual_beam_delta) % max_azimut
        return azimut, dual_beam_width
    if branch == 'R':
        azimut = (cell.azimut + dual_beam_delta) % max_azimut
        return azimut, dual_beam_width
    if cell.cell.endswith('DOT'):
        azimut = 0
        return azimut, dot_beam_width
    return cell.azimut, DEFAULT_WIDTH
