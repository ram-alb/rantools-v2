from typing import Optional


def compare_network_vs_atoll(network_params: dict, atoll_params: Optional[dict]) -> list:
    """Compare network parameters with Atoll parameters and return differences."""
    if atoll_params is None:
        return [
            {
                'site': network_params['site'],
                'cell': network_params['cell'],
                'parameter': param_name,
                'network_value': network_params[param_name],
                'atoll_value': None,
            } for param_name in network_params
        ]

    diffs = []

    for param_name in network_params.keys():
        if network_params[param_name] != atoll_params[param_name]:
            diff = {
                'site': network_params['site'],
                'cell': network_params['cell'],
                'parameter': param_name,
                'network_value': network_params[param_name],
                'atoll_value': atoll_params[param_name],
            }
            diffs.append(diff)

    return diffs
