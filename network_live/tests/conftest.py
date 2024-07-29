from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from openpyxl import Workbook

from users.tests.conftest import regular_user, rnpo_user


@pytest.fixture
def mock_xlsx_file():
    """Create mock XLSX file."""

    wb = Workbook()
    ws = wb.active

    cell_data = [
        ['header1', 'header2'],
        ['data1', 'data2'],
        ['data3', 'data4'],
    ]

    for row in cell_data:
        ws.append(row)

    with NamedTemporaryFile() as temp:
        wb.save(temp.name)
        temp.seek(0)
        return temp.read()


@pytest.fixture
def mock_select_data():
    """Mock select_data function."""
    return {
        'gsm': ([('data1', 'data2')], ['header1', 'header2']),
        'nr': ([('data3', 'data4')], ['header3', 'header4']),
    }
