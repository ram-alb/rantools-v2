from pathlib import Path

import pytest
from openpyxl import Workbook

from users.tests.conftest import new_user


@pytest.fixture
def mock_xlsx_file():
    """Create mock XLSX file."""
    xlsx_path = Path(__file__).resolve().parent / 'kcell_cells.xlsx'

    wb = Workbook()
    ws = wb.active

    cell_data = [
        ['header1', 'header2'],
        ['data1', 'data2'],
        ['data3', 'data4'],
    ]

    for row in cell_data:
        ws.append(row)

    wb.save(xlsx_path)

    return xlsx_path


@pytest.fixture
def mock_select_data():
    """Mock select_data function."""
    return {
        'gsm': ([('data1', 'data2')], ['header1', 'header2']),
        'nr': ([('data3', 'data4')], ['header3', 'header4']),
    }
