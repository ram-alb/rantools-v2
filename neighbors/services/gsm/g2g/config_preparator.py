from typing import Dict, List, NamedTuple, Set

from neighbors.services.enm.g2g.parser import NodeParams
from neighbors.services.excel import NeighborPair

baseline_params = {
    'aw': 'ON',
    'msRxMin': '100',
    'rac': '1',
}


class ExternalGeranRelation(NamedTuple):
    """A class representing ExternalGeranCellRelation."""

    bsc: str
    source_cell: str
    target_cell: str


def _get_unique_dicts(
    values_list: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    """Get a list of unique dicts."""
    unique_vals = {tuple(dict_val.items()) for dict_val in values_list}
    return [dict(keys_vals) for keys_vals in unique_vals]


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
    return _get_unique_dicts(geran_exteranal_cells)


def prepare_geran_external_relations(
    planned_neighbors: Set[NeighborPair],
    geran_cells: Dict[str, NodeParams],
) -> List[ExternalGeranRelation]:
    """Prepare data for ExternalGeranCellRelation configuration."""
    ext_geran_relations = []
    for nbr_pair in planned_neighbors:
        source_cell = nbr_pair.source_cell
        ext_relation = ExternalGeranRelation(
            bsc=geran_cells[source_cell]['bsc'],
            source_cell=source_cell,
            target_cell=nbr_pair.target_cell,
        )
        ext_geran_relations.append(ext_relation)
    return ext_geran_relations
