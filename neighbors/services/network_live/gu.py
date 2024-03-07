from typing import Callable, Dict, List, Set, Tuple, Union

from neighbors.services.excel import NeighborPair
from neighbors.services.network_live.split_neighbors import (
    InterRatNeighbors,
    IntraRatNeighbors,
    split_inter_rat_neighbors,
    split_intra_rat_neighbors,
)
from neighbors.services.network_live.tables import Cell, GsmTable, WcdmaTable
from services.db.connector import DBConnector

SplitFuncArgs = Tuple[Callable, Tuple[List[Cell], ...]]


def split_gu_neighbors(
    planned_neighbors: Set[NeighborPair],
    nbr_direction: str,
) -> Union[InterRatNeighbors, IntraRatNeighbors]:
    """Split GU planned neighbors according to nbr direction."""
    gsm_table = GsmTable(DBConnector.get_connection())
    gsm_network_cells = gsm_table.get_enm_cells()

    wcdma_table = WcdmaTable(DBConnector.get_connection())
    wcdma_network_cells = wcdma_table.get_enm_cells()

    split_data: Dict[str, SplitFuncArgs] = {
        'G2U': (split_inter_rat_neighbors, (gsm_network_cells, wcdma_network_cells)),
        'U2G': (split_inter_rat_neighbors, (wcdma_network_cells, gsm_network_cells)),
        'G2G': (split_intra_rat_neighbors, (gsm_network_cells,)),
        'U2U': (split_intra_rat_neighbors, (wcdma_network_cells,)),
    }

    split_func, network_cells = split_data[nbr_direction]

    return split_func(planned_neighbors, *network_cells)
