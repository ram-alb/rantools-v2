from neighbors.services.enm.g2g.g2g import EnmG2GData

_gsm_power_control_dl = {
    'gcell1': {'bsc': 'BSC1', 'bsPwr': '42', 'bsTxPwr': '42'},
    'gcell2': {'bsc': 'BSC1', 'bsPwr': '42', 'bsTxPwr': '42'},
    'gcell3': {'bsc': 'BSC2', 'bsPwr': '42', 'bsTxPwr': '42'},
}

_gsm_power_control_ul = {
    'gcell1': {'bsc': 'BSC1', 'bsRxMin': '14', 'bsRxSuff': '15', 'msRxSuff': '88', 'msTxPwr': '33'},
    'gcell2': {'bsc': 'BSC1', 'bsRxMin': '14', 'bsRxSuff': '15', 'msRxSuff': '88', 'msTxPwr': '33'},
    'gcell3': {'bsc': 'BSC2', 'bsRxMin': '14', 'bsRxSuff': '15', 'msRxSuff': '88', 'msTxPwr': '33'},
}

_hierarchical_cell_structure = {
    'gcell1': {
        'bsc': 'BSC1',
        'fastMsReg': 'OFF',
        'layer': '6',
        'layerHyst': '2',
        'layerThr': '-88',
        'pSsTemp': '0',
        'pTimTemp': '0',
    },
    'gcell2': {
        'bsc': 'BSC1',
        'fastMsReg': 'OFF',
        'layer': '6',
        'layerHyst': '2',
        'layerThr': '-88',
        'pSsTemp': '0',
        'pTimTemp': '0',
    },
    'gcell3': {
        'bsc': 'BSC2',
        'fastMsReg': 'OFF',
        'layer': '6',
        'layerHyst': '2',
        'layerThr': '-88',
        'pSsTemp': '0',
        'pTimTemp': '0',
    },
}

_geran_cells = {
    'gcell1': {
        'bsc': 'BSC1',
        'bcc': '6',
        'bcchNo': '10',
        'cgi': '401-02-10-1',
        'cSysType': 'GSM900',
        'ncc': '1',
    },
    'gcell2': {
        'bsc': 'BSC1',
        'bcc': '6',
        'bcchNo': '11',
        'cgi': '401-02-10-2',
        'cSysType': 'GSM900',
        'ncc': '2',
    },
    'gcell3': {
        'bsc': 'BSC2',
        'bcc': '6',
        'bcchNo': '12',
        'cgi': '401-02-10-3',
        'cSysType': 'GSM900',
        'ncc': '3',
    },
}

enm_g2g_data = EnmG2GData(
    power_control_dl=_gsm_power_control_dl,
    power_control_ul=_gsm_power_control_ul,
    hierarchical_cell_structure=_hierarchical_cell_structure,
    geran_cells=_geran_cells,
)
