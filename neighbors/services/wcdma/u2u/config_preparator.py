from typing import Dict, List, Set

from neighbors.services.enm.u2u.parser import NodeParams
from neighbors.services.excel import NeighborPair
from neighbors.services.utils import get_unique_dicts

baseline_params = {
    'individualOffset': 0,
    'qQualMin': -18,
    'qRxLevMin': -115,
}


def prepare_utran_external_cells(
    planned_neighbors: Set[NeighborPair],
    utran_cells: Dict[str, NodeParams],
) -> List[Dict[str, str]]:
    """Prepare data for ExternalUtranCell configuration."""
    external_utran_cells = []

    for nbr_pair in planned_neighbors:
        source_cell, target_cell = nbr_pair
        ext_cell = {
            'source_rnc': utran_cells[source_cell]['rnc'],
            'cell': target_cell,
            **baseline_params,
            **utran_cells[target_cell],
        }
        external_utran_cells.append(ext_cell)

    return get_unique_dicts(external_utran_cells)


def prepare_relations(
    planned_neighbors: Set[NeighborPair],
    utran_cells: Dict[str, NodeParams],
) -> List[Dict[str, str]]:
    """Prepare data for inter RNC UtranRelation configuration."""
    utran_relations = []
    for nbr_pair in planned_neighbors:
        source_cell, target_cell = nbr_pair
        relation = {
            'source_rnc': utran_cells[source_cell]['rnc'],
            'target_rnc': utran_cells[target_cell]['rnc'],
            'source_cell': source_cell,
            'target_cell': target_cell,
        }
        utran_relations.append(relation)
    return utran_relations
