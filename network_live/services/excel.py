"""Create excel file with network live cell data."""

import os
from openpyxl import Workbook
from django.conf import settings


def create_excel(network_live_data):
    """
    Create excel file with network live cell data.

    Args:
        network_live_data: dict
    """
    file_name = 'kcell_cells.xlsx'
    file_directory = os.path.join(settings.BASE_DIR, 'network_live/file')  # Define the directory within the project
    file_path = os.path.join(file_directory, file_name)
    # os.remove(file_path)
    headers = {
        'lte': [
            'SubNetwork',
            'NODEID',
            'SITENAME',
            'EUTRANCELL',
            'TAC',
            'CELLID',
            'ECI',
            'EARFCNDL',
            'QRXLEVMIN',
            'ADMINISTRATIVESTATE',
            'RACHROOTSEQUENCE',
            'PHYSICALCELLID',
            'CELLRANGE',
            'VENDOR',
            'IPADDRESS',
            'OSS',
            'AZIMUT',
            'HEIGHT',
            'LONGITUDE',
            'LATITUDE',
            'INSERTDATE',
            'primaryPlmnReserved',
        ],
        'wcdma': [
            'OPERATOR',
            'RNCID',
            'RNCNAME',
            'SITENAME',
            'UTRANCELL',
            'LOCALCELLID',
            'CID',
            'UARFCNDL',
            'UARFCNUL',
            'PSC',
            'LAC',
            'RAC',
            'SAC',
            'URALIST',
            'PRIMARYCPICHPOWER',
            'MAXIMUMTRANSMISSIONPOWER',
            'QRXLEVMIN',
            'QQUALMIN',
            'IUBLINK',
            'MOCNCELLPROFILE',
            'ADMINISTRATIVESTATE',
            'IPADDRESS',
            'VENDOR',
            'OSS',
            'AZIMUT',
            'HEIGHT',
            'LONGITUDE',
            'LATITUDE',
            'INSERTDATE',
        ],
        'gsm': [
            'OPERATOR',
            'BSCID',
            'BSCNAME',
            'SITENAME',
            'CELL',
            'BCC',
            'NCC',
            'LAC',
            'CELLID',
            'BCCH',
            'HSN',
            'MAIO',
            'TCHFREQS',
            'CELLSTATE',
            'VENDOR',
            'OSS',
            'AZIMUT',
            'HEIGHT',
            'LONGITUDE',
            'LATITUDE',
            'INSERTDATE',
        ],
        'nr': [
            'SUBNETWORK',
            'GNBID',
            'SITENAME',
            'CELLNAME',
            'CELLID',
            'CELLSTATE',
            'NCI',
            'NRPCI',
            'NRTAC',
            'RACHROOTSEQUENCE',
            'QRXLEVMIN',
            'ARFCNDL',
            'BSCHANNELBWDL',
            'CONFIGUREDMAXTXPOWER',
            'IPADDRESS',
            'VENDOR',
            'OSS',
            'AZIMUT',
            'HEIGHT',
            'LONGITUDE',
            'LATITUDE',
            'INSERTDATE',
            'SSBFREQUENCY',
        ],
    }

    work_book = Workbook()

    for technology, cell_data in network_live_data.items():
        row = 1
        column = 1
        work_sheet = work_book.create_sheet(technology.upper())
        for header in headers[technology]:
            work_sheet.cell(row=row, column=column, value=header)
            column += 1

        row += 1
        column = 1

        for cell_values in cell_data:
            for value in cell_values:
                work_sheet.cell(row=row, column=column, value=value)
                column += 1
            column = 1
            row += 1

    work_book.remove_sheet(work_book.get_sheet_by_name('Sheet'))
    work_book.save(file_path)
    return file_path
