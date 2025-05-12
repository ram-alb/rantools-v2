from typing import Optional


def _create_diff(network_params: dict, param_name: str, network_value, atoll_vlaue) -> dict:
    """Create a dictionary representing the difference between network and Atoll parameters."""
    return {
        'site': network_params['site'],
        'cell': network_params['cell'],
        'parameter': param_name,
        'network_value': network_value,
        'atoll_value': atoll_vlaue,
    }


def compare_network_vs_atoll(
    network_params: dict,
    atoll_params: Optional[dict],
    technology: Optional[str] = None,
) -> list:
    """Compare network parameters with Atoll parameters and return differences."""
    if atoll_params is None:
        return [
            _create_diff(network_params, param_name, network_params[param_name], None)
            for param_name in network_params
        ]

    diffs = []

    for param_name in network_params.keys():
        net_val = network_params[param_name]
        atoll_val = atoll_params.get(param_name)

        if technology == 'LTE' and param_name == 'site':
            if net_val not in {atoll_val, atoll_params['lte_sitename']}:
                diffs.append(
                    _create_diff(network_params, param_name, net_val, atoll_val),
                )
        elif net_val != atoll_val:
            diffs.append(
                _create_diff(network_params, param_name, net_val, atoll_val),
            )

    return diffs
