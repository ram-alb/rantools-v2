def handle_diffs(node, diffs):
    """
    Sort the diffs by nodes.

    Args:
        node (str): a node name
        diffs (list): a list of dicts with parameters diffs

    Returns:
        dict: keys - node names, values - list of dicts with diffs
    """
    diff_by_nodes = {
        'Total': diffs,
    }
    for diff in diffs:
        diff_by_nodes.setdefault(diff[node], []).append(diff)

    return diff_by_nodes
