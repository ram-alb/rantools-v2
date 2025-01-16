import os
import zipfile
from typing import Dict, List

import openpyxl

REPORTS_DIR = 'day_x/network_live_files/'


def _add_sheet(workbook, sheet_name: str, headers: List[str], sheet_data: List[tuple]) -> None:
    """Add a sheet to the workbook with the given headers and data."""
    sheet = workbook.create_sheet(sheet_name)
    sheet.append(headers)
    for row in sheet_data:
        sheet.append(row)


def _compress_file(file_path: str, archive_name: str = None) -> str:
    """Compress an Excel file into a ZIP archive."""
    if archive_name is None:
        archive_name = os.path.splitext(file_path)[0] + '.zip'

    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.write(file_path, arcname=os.path.basename(file_path))

    return archive_name


def fill_excel(network_live_data: Dict[str, List[tuple]]) -> None:
    """Fill excel file with network live data."""
    gsm_wcdma_headers = [
        'BS_NAME',
        'BS_ID',
        'BS_LAC',
        'BS_CELL',
        'Cell',
        'BS_LONGITUDE',
        'BS_LATITUDE',
        'Technology',
        'BSIC or SC',
        'Controller',
        'FREE',
        'BS_CELL',
    ]

    lte_headers = [
        'BS_NAME',
        'BS_ID',
        'BS_TAC',
        'BS_CELL',
        'BS_LONGITUDE',
        'BS_LATITUDE',
        'Technology',
        'ENodeBId',
        'CellId',
        'PhysicalCellIdentifier',
        'Region',
    ]

    wb = openpyxl.Workbook()

    _add_sheet(wb, '23G', gsm_wcdma_headers, network_live_data['GSM'] + network_live_data['WCDMA'])
    _add_sheet(wb, '4G', lte_headers, network_live_data['LTE'])
    wb.remove(wb['Sheet'])

    report_name = 'DEC_2019.xlsx'
    report_path = f'{REPORTS_DIR}{report_name}'
    wb.save(report_path)

    return _compress_file(report_path)
