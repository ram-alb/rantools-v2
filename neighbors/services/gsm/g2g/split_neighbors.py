from typing import Dict, List, NamedTuple, Set

from neighbors.services.enm.g2g.parser import NodeParams
from neighbors.services.excel import NeighborPair


class IntraInterNeighbors(NamedTuple):
    """A class represeting planned neighbors splitted to intra and inter bsc neighbors."""

    intra_bsc_neighbors: Set[NeighborPair]
    inter_bsc_neighbors: Set[NeighborPair]


def split_neighbors_by_bsc(
    planned_neighbors: List[NeighborPair],
    enm_geran_cells: Dict[str, NodeParams],
) -> IntraInterNeighbors:
    """Split planned neighbors to intra bsc and inter bsc neighbors."""
    intra_bsc_neighbors = set()
    inter_bsc_neighbors = set()

    for nbr_pair in planned_neighbors:
        source_cell_bsc = enm_geran_cells[nbr_pair.source_cell]['bsc']
        target_cell_bsc = enm_geran_cells[nbr_pair.target_cell]['bsc']
        if source_cell_bsc == target_cell_bsc:
            intra_bsc_neighbors.add(nbr_pair)
        else:
            inter_bsc_neighbors.add(nbr_pair)

    return IntraInterNeighbors(
        intra_bsc_neighbors=intra_bsc_neighbors,
        inter_bsc_neighbors=inter_bsc_neighbors,
    )
