import io
from typing import List, NamedTuple

import openpyxl


class NeighborPair(NamedTuple):
    """A NamedTuple representing neighbor cells pair."""

    source_cell: str
    target_cell: str


def get_neighbor_cells_from_excel(excel_file: io.BytesIO) -> List[NeighborPair]:
    """Get a neighbor pairs list from an Excel file."""
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active

    neighbors = []
    start_row = 2
    for row in sheet.iter_rows(min_row=start_row, values_only=True):  # type: ignore
        neighbors.append(NeighborPair(*row))

    workbook.close()

    return neighbors
