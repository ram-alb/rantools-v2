def categorize_planned_neighbors(planned_neighbors, source_cells, target_cells):
    """Categorize planned neighbors into existing and nonexistent cells."""
    nonexistent_cells = []
    valid_neighbors = []

    for nbr_pair in planned_neighbors:
        if nbr_pair.source_cell in source_cells and nbr_pair.target_cell in target_cells:
            valid_neighbors.append(nbr_pair)
        else:
            nonexistent_cells.append(nbr_pair)

    return valid_neighbors, nonexistent_cells
