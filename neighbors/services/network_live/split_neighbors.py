from typing import Dict, List, NamedTuple, Set

from neighbors.services.excel import NeighborPair
from neighbors.services.network_live.tables import Cell


class InterRatNeighbors(NamedTuple):
    """A class representing data with inter rat neighbors."""

    existing_cells: List[NeighborPair]
    non_existing_cells: List[NeighborPair]
    source_controllers: Set[str]
    target_controllers: Set[str]


class IntraRatNeighbors(NamedTuple):
    """A class representing data with intra rat neighbors."""

    inter_controllers_neighbors: Set[NeighborPair]
    intra_controller_neighbors: Set[NeighborPair]
    controllers: Set[str]
    non_existing_cells: List[NeighborPair]


class LteNeighbors(NamedTuple):
    """A class representing data with LTE earfcn for mobility to LTE."""

    existing_cells: List[NeighborPair]
    controllers: Dict[str, str]
    non_existing_cells: List[NeighborPair]


def split_inter_rat_neighbors(
    planned_neighbors: Set[NeighborPair],
    nl_source_cells: List[Cell],
    nl_target_cells: List[Cell],
) -> InterRatNeighbors:
    """Split planned neighbors into existing and non existing cells."""
    existing_cells = []
    non_existing_cells = []
    source_controllers = set()
    target_controllers = set()

    source_cells = {cell: controller for controller, cell in nl_source_cells}
    target_cells = {cell: controller for controller, cell in nl_target_cells}

    for nbr_pair in planned_neighbors:
        source_cell, target_cell = nbr_pair
        if source_cell in source_cells and target_cell in target_cells:
            existing_cells.append(nbr_pair)
            source_controllers.add(source_cells[source_cell])
            target_controllers.add(target_cells[target_cell])
        else:
            non_existing_cells.append(nbr_pair)

    return InterRatNeighbors(
        existing_cells,
        non_existing_cells,
        source_controllers,
        target_controllers,
    )


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

    for nbr_pair in planned_neighbors:
        source_cell, target_cell = nbr_pair
        if source_cell in network_cells and target_cell in network_cells:
            source_controller = network_cells[source_cell]
            target_controller = network_cells[target_cell]
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


def split_lte_neighbors(
    planned_neighbors: Set[NeighborPair],
    network_live_cells: List[Cell],
) -> LteNeighbors:
    """Split planned neighbors into existing cells and non existing."""
    existing_cells = []
    non_existing_cells = []
    controllers = {}

    network_cells = {cell: controller for controller, cell in network_live_cells}

    for nbr_pair in planned_neighbors:
        source_cell = nbr_pair.source
        if source_cell in network_cells:
            existing_cells.append(nbr_pair)
            controllers[source_cell] = network_cells[source_cell]
        else:
            non_existing_cells.append(nbr_pair)

    return LteNeighbors(
        existing_cells=existing_cells,
        controllers=controllers,
        non_existing_cells=non_existing_cells,
    )
