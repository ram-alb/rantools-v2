from typing import Dict, List, Set

from neighbors.services.enm.g2g.parser import NodeParams
from neighbors.services.excel import NeighborPair

baseline_params = {
    'aw': 'ON',
    'msRxMin': '100',
    'rac': '1',
}


def prepare_geran_external_cells(
    planned_neighbors: Set[NeighborPair],
    geran_cells: Dict[str, NodeParams],
    power_control_dl_params: Dict[str, NodeParams],
    power_control_ul_params: Dict[str, NodeParams],
    hierarchical_cell_structure: Dict[str, NodeParams],
) -> List[Dict[str, str]]:
    """Prepare data for ExternalGeranCell configuration."""
    geran_exteranal_cells = []
    for nbr_pair in planned_neighbors:
        source = nbr_pair.source_cell
        target = nbr_pair.target_cell
        ext_cell = {
            'cell': target,
            **baseline_params,
            **geran_cells[target],
            **power_control_dl_params[target],
            **power_control_ul_params[target],
            **hierarchical_cell_structure[target],
        }
        ext_cell['bsc'] = geran_cells[source]['bsc']
        geran_exteranal_cells.append(ext_cell)
    return geran_exteranal_cells
