from dataclasses import dataclass
from pathlib import Path

import openpyxl


@dataclass
class NeighborPair:
    """A dataclass representing neighbor cells pair."""

    source_cell: str
    target_cell: str


def is_excel_file(filename):
    """Check is a provided filename is Excel file or not."""
    allowed_extensions = {'.xlsx', '.xls'}
    extension = Path(filename).suffix
    return extension in allowed_extensions


def get_neighbor_cells_from_excel(excel_file):
    """Get a neighbor pairs list from an Excel file."""
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active

    neighbors = []
    start_row = 2
    for row in sheet.iter_rows(min_row=start_row, values_only=True):
        neighbors.append(NeighborPair(*row))

    workbook.close()

    return neighbors