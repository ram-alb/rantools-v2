from neighbors.services.enm.wcdma.u2g import EnmU2GData

_geran_cells = {
    'gcell1': {
        'bcc': '1',
        'bcchNo': '1',
        'lac': '10',
        'ci': '1',
        'ncc': '7',
        'band_indicator':
        'OTHER_BANDS',
        'max_tx_pwr_ul': '33',
        'qrxlev_min': '-103',
    },
    'gcell2': {
        'bcc': '2',
        'bcchNo': '2',
        'lac': '10',
        'ci': '2',
        'ncc': '7',
        'band_indicator': 'OTHER_BANDS',
        'max_tx_pwr_ul': '33',
        'qrxlev_min': '-103',
    },
    'gcell3': {
        'bcc': '3',
        'bcchNo': '3',
        'lac': '10',
        'ci': '3',
        'ncc': '7',
        'band_indicator': 'OTHER_BANDS',
        'max_tx_pwr_ul': '33',
        'qrxlev_min': '-103',
    },
}

_utran_cells = {
    'ucell1': 'RNC1',
    'ucell2': 'RNC1',
    'ucell3': 'RNC2',
}

_ext_gsm_network_ids = {'RNC1': '10', 'RNC2': '10'}

enm_u2g_data = EnmU2GData(
    geran_cell_params=_geran_cells,
    utran_cells=_utran_cells,
    ext_gsm_network_ids=_ext_gsm_network_ids,
)
