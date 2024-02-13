from typing import List

from neighbors.services.excel import NeighborPair
from neighbors.services.network_live.split_neighbors import (
    SplittedNeighbors,
    split_planned_neighbors,
)
from neighbors.services.network_live.tables import get_network_cells


def split_gu_neighbors(
    planned_neighbors: List[NeighborPair],
    nbr_direction: str,
) -> SplittedNeighbors:
    """Categorize GU planned neighbors into existing and non existing cells."""
    gsm_network_cells = get_network_cells('GSM')
    wcdma_network_cells = get_network_cells('WCDMA')

    network_live_cells = {
        'G2U': (gsm_network_cells, wcdma_network_cells),
        'U2G': (wcdma_network_cells, gsm_network_cells),
    }

    return split_planned_neighbors(planned_neighbors, *network_live_cells[nbr_direction])
