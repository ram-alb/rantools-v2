import os
from typing import Dict, NamedTuple, Set

from neighbors.services.enm.wcdma.enm_cli import EnmCli
from neighbors.services.enm.wcdma.parser import (
    GerancellParameters,
    parse_external_gsm_network_ids,
    parse_gerancell_parameters,
    parse_utran_cells,
)


class EnmU2GData(NamedTuple):
    """A class representing the necessary data for U2G neighbors configuration."""

    geran_cell_params: Dict[str, GerancellParameters]
    utran_cells: Dict[str, str]
    ext_gsm_network_ids: Dict[str, str]


def get_enm_u2g_data(rnc_set: Set[str], bsc_set: Set[str]) -> EnmU2GData:
    """Get the necessary data from ENM for U2G neighbor configuration."""
    if not rnc_set or not bsc_set:
        return EnmU2GData(
            geran_cell_params={},
            utran_cells={},
            ext_gsm_network_ids={},
        )

    enm_server = os.getenv('ENM_SERVER_2')
    if enm_server is None:
        raise ValueError('No ENM_SERVER_2 environment variable')

    enm2_cli = EnmCli(enm_server, rnc_set, bsc_set)

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
