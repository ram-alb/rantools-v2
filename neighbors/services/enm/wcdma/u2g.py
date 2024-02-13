import os
from typing import NamedTuple

from neighbors.services.enm.wcdma.enm_cli import EnmCli
from neighbors.services.enm.wcdma.parser import (
    parse_external_gsm_network_ids,
    parse_gerancell_parameters,
    parse_utran_cells,
)


class EnmU2GData(NamedTuple):
    geran_cell_params: dict
    utran_cells: dict
    ext_gsm_network_ids: dict


def get_enm_u2g_data():
    enm2_cli = EnmCli(os.getenv('ENM_SERVER_2'))

    enm_gerancell_data, last_parameter = enm2_cli.get_gerancell_params()
    geran_cell_params = parse_gerancell_parameters(enm_gerancell_data, last_parameter)

    enm_utrancell_data = enm2_cli.get_utran_cells()
    utran_cells = parse_utran_cells(enm_utrancell_data)

    enm_ext_gsm_network_data = enm2_cli.get_external_gsm_network_data()
    ext_gsm_network_ids = parse_external_gsm_network_ids(enm_ext_gsm_network_data)

    return EnmU2GData(
        geran_cell_params,
        utran_cells,
        ext_gsm_network_ids,
    )
