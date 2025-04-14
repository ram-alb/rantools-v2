from deepdiff import DeepDiff


def format_diff(technology, row, deep_diff):
    """
    Format DeepDiff two dicts comparing result.

    Args:
        technology (str): a technology name
        row (namedtuple): a network params
        deep_diff (dict): DeepDiff result

    Returns:
        list: a list of dicts
    """
    node_types = {
        'LTE': 'subnetwork',
        'WCDMA': 'rnc',
        'GSM': 'bsc',
        'NR': 'subnetwork',
    }

    node = node_types[technology]

    formatted_diff = []
    for param_key, param_vals in deep_diff['values_changed'].items():
        diff = {
            node: getattr(row, node),
            'site': row.site,
            'cell': row.cell,
        }
        parameter_data = param_key.split('[')
        diff['parameter'] = parameter_data[-1][:-1]
        diff['network value'] = param_vals['old_value']
        diff['atoll value'] = param_vals['new_value']
        formatted_diff.append(diff)
    return formatted_diff


def compare(
    technology,
    selected_network_data,
    get_network_params,
    atoll_data,
    get_atoll_params,
):
    """
    Compare network parameters with atoll parameters for given technology.

    Args:
        technology (str): a technology name
        selected_network_data (list): a list of namedtuples of netwrok params
        get_network_params (func): a function to get needed network params
        atoll_data (dict): params from atoll, keys - cells, values - params
        get_atoll_params (func): a function to get needed atoll params

    Returns:
        list: a list of dicts with diffs
    """
    deltas = []
    for row in selected_network_data:
        network_params = get_network_params(row)
        atoll_params = get_atoll_params(row.cell, atoll_data)
        deep_diff = DeepDiff(network_params, atoll_params).to_dict()
        if deep_diff:
            deltas += format_diff(technology, row, deep_diff)
    return deltas
