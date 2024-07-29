import zipfile
from pathlib import Path

import pytest
from django.contrib.auth.models import Group, User
from django.test import RequestFactory

from users.tests.conftest import regular_user, rnpo_user


@pytest.fixture
def zip_file():
    """Create zip file."""
    report_path = Path(__file__).resolve().parent / 'G2U.zip'
    with zipfile.ZipFile(report_path, 'w') as zip_file:
        return report_path
