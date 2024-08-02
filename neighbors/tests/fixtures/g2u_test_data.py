from neighbors.services.enm.gsm.g2u import EnmG2UData

_rnc_params = {
    'RNC1': {'mcc': '401', 'mnc': '02', 'rncId': '1111'},
    'RNC2': {'mcc': '401', 'mnc': '02', 'rncId': '2222'},
}

_utrna_cell_params = {
    'ucell1': {
        'rnc': 'RNC1',
        'localCellId': '1',
        'LocationArea': '10',
        'primaryScramblingCode': '1',
        'uarfcnDl': '111',
    },
    'ucell2': {
        'rnc': 'RNC1',
        'localCellId': '2',
        'LocationArea': '10',
        'primaryScramblingCode': '2',
        'uarfcnDl': '111',
    },
    'ucell3': {
        'rnc': 'RNC2',
        'localCellId': '3',
        'LocationArea': '10',
        'primaryScramblingCode': '3',
        'uarfcnDl': '111',
    },
}

_wcdma_geran_cells = {
    'gcell1': 'BSC1',
    'gcell2': 'BSC1',
    'gcell3': 'BSC2',
}

enm_g2u_data = EnmG2UData(
    rnc_params=_rnc_params,
    utran_cell_params=_utrna_cell_params,
    geran_cells=_wcdma_geran_cells,
)
