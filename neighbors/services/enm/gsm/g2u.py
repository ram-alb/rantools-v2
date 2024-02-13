import os
from dataclasses import dataclass

from neighbors.services.enm.gsm.enm_cli import EnmCLI
from neighbors.services.enm.gsm.parser import (
    parse_geran_cells,
    parse_rnc_function_params,
    parse_utran_cell_params,
)


@dataclass
class EnmG2UData:
    """A data class representing the necessary data for G2U neighbors configuration."""

    rnc_params: dict
    utran_cell_params: dict
    geran_cells: dict


def get_enm_g2u_data():
    """Get the necessary data from ENM for G2U neighbor configuration."""
    enm2_cli = EnmCLI(os.getenv('ENM_SERVER_2'))

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
