from typing import Dict, NamedTuple, Set

from neighbors.services.enm.g2g.enm_cli import EnmCli
from neighbors.services.enm.g2g.parser import NodeParams, parse_enm_data
from neighbors.services.enm.utils import get_enm_server


class EnmG2GData(NamedTuple):
    """A class representing the necessary data for G2G neighbors configuration."""

    power_control_dl: Dict[str, NodeParams]
    power_control_ul: Dict[str, NodeParams]
    hierarchical_cell_structure: Dict[str, NodeParams]
    geran_cells: Dict[str, NodeParams]


def get_enm_g2g_data(bsc_set: Set[str], enm: str) -> EnmG2GData:
    """Get the necessary data from ENM for G2G neighbor configuration."""
    if not bsc_set:
        return EnmG2GData(
            power_control_dl={},
            power_control_ul={},
            hierarchical_cell_structure={},
            geran_cells={},
        )
    enm_server = get_enm_server(enm)
    enm_cli = EnmCli(enm_server, bsc_set)

    power_control_dl_data = enm_cli.get_power_control_dl_params()
    power_control_ul_data = enm_cli.get_power_control_ul_params()
    hierarchical_cell_structure_data = enm_cli.get_hierarchical_cell_structure_params()
    geran_cell_data = enm_cli.get_geran_cell_params()

    return EnmG2GData(
        power_control_dl=parse_enm_data(power_control_dl_data),
        power_control_ul=parse_enm_data(power_control_ul_data),
        hierarchical_cell_structure=parse_enm_data(hierarchical_cell_structure_data),
        geran_cells=parse_enm_data(geran_cell_data),
    )
