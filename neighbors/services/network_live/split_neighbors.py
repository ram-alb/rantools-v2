from typing import List, NamedTuple, Set

from neighbors.services.excel import NeighborPair
from neighbors.services.network_live.tables import Cell


class InterRatNeighbors(NamedTuple):
    """A class representing data with inter rat neighbors."""

    existing_cells: List[NeighborPair]
    non_existing_cells: List[NeighborPair]


class IntraRatNeighbors(NamedTuple):
    inter_controllers_neighbors: Set[NeighborPair]
    intra_controller_neighbors: Set[NeighborPair]
    controllers: Set[str]
    non_existing_cells: List[NeighborPair]


def split_inter_rat_neighbors(
    planned_neighbors: Set[NeighborPair],
    source_cells: List[Cell],
    target_cells: List[Cell],
) -> InterRatNeighbors:
    """Split planned neighbors into existing and non existing cells."""
    existing_cells = []
    non_existing_cells = []

    for nbr_pair in planned_neighbors:
        if nbr_pair.source_cell in source_cells and nbr_pair.target_cell in target_cells:
            existing_cells.append(nbr_pair)
        else:
            non_existing_cells.append(nbr_pair)

    return InterRatNeighbors(existing_cells, non_existing_cells)


def split_intra_rat_neighbors(
    planned_neighbors: Set[NeighborPair],
    network_live_cells: List[Cell],
) -> IntraRatNeighbors:
    """Split planned neighbors into intra/inter controller neighbors and non existing cells."""
    intra_controller_neighbors = set()
    inter_controllers_neighbors = set()
    controllers = set()
    non_existing_cells = []

    network_cells = {
        cell: controller for controller, cell in network_live_cells
    }

    print(planned_neighbors)

    for nbr_pair in planned_neighbors:
        source_cell, target_cell = nbr_pair
        source_controller = network_cells[source_cell]
        target_controller = network_cells[target_cell]
        if source_cell in network_cells and target_cell in network_cells:
            if source_controller == target_controller:
                intra_controller_neighbors.add(nbr_pair)
                controllers.add(source_controller)
            else:
                inter_controllers_neighbors.add(nbr_pair)
                controllers.update((source_controller, target_controller))
        else:
            non_existing_cells.append(nbr_pair)

    return IntraRatNeighbors(
        inter_controllers_neighbors=inter_controllers_neighbors,
        intra_controller_neighbors=intra_controller_neighbors,
        controllers=controllers,
        non_existing_cells=non_existing_cells,
    )
