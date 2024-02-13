from typing import List, NamedTuple, Set

from neighbors.services.excel import NeighborPair


class SplittedNeighbors(NamedTuple):
    """A class representing splitted neighbor cells."""

    existing_cells: List[NeighborPair]
    non_existing_cells: List[NeighborPair]


def split_planned_neighbors(
    planned_neighbors: List[NeighborPair],
    source_cells: Set[str],
    target_cells: Set[str],
) -> SplittedNeighbors:
    """Split planned neighbors into existing and non existing cells."""
    existing_cells = []
    non_existing_cells = []

    for nbr_pair in planned_neighbors:
        if nbr_pair.source_cell in source_cells and nbr_pair.target_cell in target_cells:
            existing_cells.append(nbr_pair)
        else:
            non_existing_cells.append(nbr_pair)

    return SplittedNeighbors(existing_cells, non_existing_cells)
