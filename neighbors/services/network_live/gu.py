from typing import List

from neighbors.services.excel import NeighborPair
from neighbors.services.network_live.split_neighbors import (
    SplittedNeighbors,
    split_planned_neighbors,
)
from neighbors.services.network_live.tables import GsmTable, WcdmaTable
from services.db.connector import DBConnector


def split_gu_neighbors(
    planned_neighbors: List[NeighborPair],
    nbr_direction: str,
) -> SplittedNeighbors:
    """Split GU planned neighbors into existing and non existing cells."""
    gsm_table = GsmTable(DBConnector.get_connection())
    gsm_network_cells = gsm_table.get_enm_cells()

    wcdma_table = WcdmaTable(DBConnector.get_connection())
    wcdma_network_cells = wcdma_table.get_enm_cells()

    network_live_cells = {
        'G2U': (gsm_network_cells, wcdma_network_cells),
        'U2G': (wcdma_network_cells, gsm_network_cells),
    }

    return split_planned_neighbors(planned_neighbors, *network_live_cells[nbr_direction])
