from typing import List, Optional


def _create_diff(network_params: dict, param_name: str, network_value, atoll_vlaue) -> dict:
    """Create a dictionary representing the difference between network and Atoll parameters."""
    return {
        'site': network_params['site'],
        'cell': network_params['cell'],
        'parameter': param_name,
        'network_value': network_value,
        'atoll_value': atoll_vlaue,
    }


def _compare_network_vs_atoll(
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


def calculate_diffs(
    network_data: List[dict],
    atoll_data: dict,
    technology: Optional[str] = None,
) -> dict:
    """Calculate differences between network and Atoll data."""
    diffs = {}

    for row in network_data:
        network_params = row._asdict()
        subnetwork = network_params.pop('subnetwork', None)
        atoll_cell_params = atoll_data.get(network_params['cell'], None)
        diff = _compare_network_vs_atoll(network_params, atoll_cell_params, technology=technology)
        if diff:
            diffs.setdefault(subnetwork, []).extend(diff)

    return diffs


def aggregate_diffs(diffs: dict) -> tuple:
    """Aggregate differences by subnetwork and return total count and counts per subnetwork."""
    diff_count_by_subnetwork = dict(sorted(
        ((subnetwork, len(diff)) for subnetwork, diff in diffs.items()),
        key=lambda diff_item: diff_item[0],
    ))

    total_diff_count = sum(diff_count_by_subnetwork.values())

    return total_diff_count, diff_count_by_subnetwork
