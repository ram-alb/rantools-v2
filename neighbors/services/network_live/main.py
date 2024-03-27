from typing import Set

from neighbors.services.excel import NeighborPair
from neighbors.services.network_live.split_neighbors import (
    InterRatNeighbors,
    IntraRatNeighbors,
    LteNeighbors,
    split_inter_rat_neighbors,
    split_intra_rat_neighbors,
    split_lte_neighbors,
)
from neighbors.services.network_live.tables import GsmTable, WcdmaTable
from services.db.connector import DBConnector


def split_gu_neighbors(
    planned_neighbors: Set[NeighborPair],
    nbr_direction: str,
    enm: str,
) -> InterRatNeighbors:
    """Split GU planned neighbors according to nbr direction."""
    gsm_table = GsmTable(DBConnector.get_connection())
    gsm_network_cells = gsm_table.get_enm_cells(enm)

    wcdma_table = WcdmaTable(DBConnector.get_connection())
    wcdma_network_cells = wcdma_table.get_enm_cells(enm)

    network_live_data = {
        'G2U': (gsm_network_cells, wcdma_network_cells),
        'U2G': (wcdma_network_cells, gsm_network_cells),
    }

    network_cells = network_live_data[nbr_direction]

    return split_inter_rat_neighbors(planned_neighbors, *network_cells)


def split_g2g_neighbors(
    planned_neighbors: Set[NeighborPair],
    enm: str,
) -> IntraRatNeighbors:
    """Split G2G planned neighbors."""
    gsm_table = GsmTable(DBConnector.get_connection())
    gsm_network_cells = gsm_table.get_enm_cells(enm)
    return split_intra_rat_neighbors(planned_neighbors, gsm_network_cells)


def split_g2l_neighbors(
    planned_neighbors: Set[NeighborPair],
    enm: str,
) -> LteNeighbors:
    """Split G2L planned neighbors."""
    gsm_table = GsmTable(DBConnector.get_connection())
    gsm_network_cells = gsm_table.get_enm_cells(enm)
    return split_lte_neighbors(planned_neighbors, gsm_network_cells)


def split_u2u_neighbors(
    planned_neighbors: Set[NeighborPair],
    enm: str,
) -> IntraRatNeighbors:
    """Split U2U planned neighbors."""
    wcdma_table = WcdmaTable(DBConnector.get_connection())
    wcdma_network_cells = wcdma_table.get_enm_cells(enm)
    return split_intra_rat_neighbors(planned_neighbors, wcdma_network_cells)


def split_u2l_neighbors(
    planned_neighbors: Set[NeighborPair],
    enm: str,
) -> LteNeighbors:
    """Split U2L planned neighbors."""
    wcdma_table = WcdmaTable(DBConnector.get_connection())
    wcdma_network_cells = wcdma_table.get_enm_cells(enm)
    return split_lte_neighbors(planned_neighbors, wcdma_network_cells)
