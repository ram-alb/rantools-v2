"""Create excel file with network live cell data."""

import os
from typing import Dict, List, Tuple

from django.conf import settings
from openpyxl import Workbook

InnerTuple = Tuple[List[Tuple], List[str]]


def create_excel(network_live_data: Dict[str, InnerTuple]) -> str:
    """Create excel file with network live cell data."""
    file_name = 'kcell_cells.xlsx'
    file_directory = os.path.join(settings.BASE_DIR, 'network_live/file')
    file_path = os.path.join(file_directory, file_name)

    work_book = Workbook()

    for technology, (cell_data, headers) in network_live_data.items():
        work_sheet = work_book.create_sheet(technology.upper())

        row = 1
        for column, header in enumerate(headers, start=1):
            work_sheet.cell(row=row, column=column, value=header)

        row = 2  # Start after headers
        for cell_values in cell_data:
            work_sheet.append(cell_values)
            row += 1

    work_book.remove(work_book['Sheet'])
    work_book.save(file_path)
    return file_path
