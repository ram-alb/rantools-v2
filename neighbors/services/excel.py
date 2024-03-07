import io
from typing import NamedTuple, Set

import openpyxl


class NeighborPair(NamedTuple):
    """A NamedTuple representing neighbor cells pair."""

    source_cell: str
    target_cell: str


def get_neighbor_cells_from_excel(excel_file: io.BytesIO) -> Set[NeighborPair]:
    """Get a neighbor pairs list from an Excel file."""
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active

    neighbors = set()
    start_row = 2
    for row in sheet.iter_rows(min_row=start_row, values_only=True):  # type: ignore
        source_cell, target_cell = row
        if all((source_cell, target_cell)):
            neighbors.add(NeighborPair(source_cell, target_cell))

    workbook.close()

    return neighbors
