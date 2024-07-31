import zipfile
from pathlib import Path

import pytest


@pytest.fixture
def zip_file():
    """Create zip file."""
    report_path = Path(__file__).resolve().parent / 'G2U.zip'
    with zipfile.ZipFile(report_path, 'w') as zip_file:
        return report_path
