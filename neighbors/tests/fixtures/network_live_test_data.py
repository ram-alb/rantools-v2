from neighbors.services.network_live.tables import Cell

gsm_network_cells = [
    Cell(controller='BSC1', cell='gcell1'),
    Cell(controller='BSC1', cell='gcell2'),
    Cell(controller='BSC2', cell='gcell3'),
]

wcdma_network_cells = [
    Cell(controller='RNC1', cell='ucell1'),
    Cell(controller='RNC1', cell='ucell2'),
    Cell(controller='RNC2', cell='ucell3'),
]
