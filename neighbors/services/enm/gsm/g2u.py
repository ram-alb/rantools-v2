from typing import Dict, NamedTuple, Set

from neighbors.services.enm.gsm.enm_cli import EnmCLI
from neighbors.services.enm.gsm.parser import (
    NodeParams,
    parse_geran_cells,
    parse_rnc_function_params,
    parse_utran_cell_params,
)
from neighbors.services.enm.utils import get_enm_server


class EnmG2UData(NamedTuple):
    """A class representing the necessary data for G2U neighbors configuration."""

    rnc_params: Dict[str, NodeParams]
    utran_cell_params: Dict[str, NodeParams]
    geran_cells: Dict[str, str]


def get_enm_g2u_data(bsc_set: Set[str], rnc_set: Set[str], enm: str) -> EnmG2UData:
    """Get the necessary data from ENM for G2U neighbor configuration."""
    if not bsc_set or not rnc_set:
        return EnmG2UData(
            rnc_params={},
            utran_cell_params={},
            geran_cells={},
        )

    enm_server = get_enm_server(enm)
    enm2_cli = EnmCLI(enm_server, bsc_set, rnc_set)

    enm_rnc_function_params, rnc_last_parameter = enm2_cli.get_rnc_function_params()
    rnc_params = parse_rnc_function_params(enm_rnc_function_params, rnc_last_parameter)

    enm_utran_cell_params, cell_last_parameter = enm2_cli.get_utrancell_params()
    utran_cell_params = parse_utran_cell_params(enm_utran_cell_params, cell_last_parameter)

    enm_geran_cells = enm2_cli.get_geran_cells()
    geran_cells = parse_geran_cells(enm_geran_cells)

    return EnmG2UData(
        rnc_params=rnc_params,
        utran_cell_params=utran_cell_params,
        geran_cells=geran_cells,
    )
