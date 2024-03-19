import os
from typing import Dict, Set

from neighbors.services.enm.u2u.enm_cli import EnmCli
from neighbors.services.enm.u2u.parser import NodeParams, parse_utran_cell_params


def get_u2u_enm_data(rnc_set: Set[str]) -> Dict[str, NodeParams]:
    """Get the necessary data from ENM for U2U neighbor configuration."""
    if not rnc_set:
        return {}

    enm_server = os.getenv('ENM_SERVER_2')
    if enm_server is None:
        raise ValueError('No ENM_SERVER_2 environment variable')

    enm2_cli = EnmCli(enm_server, rnc_set)

    enm_utran_cell_data = enm2_cli.get_utran_cell_params()

    return parse_utran_cell_params(enm_utran_cell_data)
