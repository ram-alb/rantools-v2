from typing import Dict, List, Optional, Tuple, Union

from network_vs_atoll.services.lte.sql import NetworkRow as LteNetworkRow
from network_vs_atoll.services.nr.sql import NetworkRow as NrNetworkRow
from network_vs_atoll.services.utils import AtollParams, CellParams, ParameterValue

NetworkRow = Union[LteNetworkRow, NrNetworkRow]
Diff = Dict[str, ParameterValue]
Diffs = Dict[Optional[str], List[Diff]]
CountByNode = Dict[Optional[str], int]
AggregatedDiffs = Tuple[int, CountByNode]


def _create_diff(
    network_params: CellParams,
    param_name: str,
    atoll_vlaue: ParameterValue,
) -> Diff:
    """Create a dictionary representing the difference between network and Atoll parameters."""
    return {
        'site': network_params['site'],
        'cell': network_params['cell'],
        'parameter': param_name,
        'network_value': network_params[param_name],
        'atoll_value': atoll_vlaue,
    }


def _compare_network_vs_atoll(
    network_params: CellParams,
    atoll_params: Optional[CellParams],
    technology: Optional[str] = None,
) -> List[Diff]:
    """Compare network parameters with Atoll parameters and return differences."""
    if atoll_params is None:
        return [
            _create_diff(network_params, param_name, None)
            for param_name in network_params
        ]

    diffs = []

    for param_name in network_params.keys():
        net_val = network_params[param_name]
        atoll_val = atoll_params.get(param_name)

        if technology == 'LTE' and param_name == 'site':
            if net_val not in {atoll_val, atoll_params['lte_sitename']}:
                diffs.append(
                    _create_diff(network_params, param_name, atoll_val),
                )
        elif net_val != atoll_val:
            diffs.append(
                _create_diff(network_params, param_name, atoll_val),
            )

    return diffs


def calculate_diffs(
    network_data: List[NetworkRow],
    atoll_data: AtollParams,
    technology: Optional[str] = None,
) -> Diffs:
    """Calculate differences between network and Atoll data."""
    diffs: Diffs = {}

    for row in network_data:
        network_params = row._asdict()
        subnetwork = network_params.pop('subnetwork', None)
        atoll_cell_params = atoll_data.get(network_params['cell'], None)
        diff = _compare_network_vs_atoll(network_params, atoll_cell_params, technology=technology)
        if diff:
            diffs.setdefault(subnetwork, []).extend(diff)

    return diffs


def aggregate_diffs(diffs: Diffs) -> AggregatedDiffs:
    """Aggregate differences by subnetwork and return total count and counts per subnetwork."""
    diff_count_by_subnetwork = dict(sorted(
        ((subnetwork, len(diff)) for subnetwork, diff in diffs.items()),
        key=lambda diff_count: (diff_count[0] is None, diff_count[0] or ''),
    ))

    total_diff_count = sum(diff_count_by_subnetwork.values())

    return total_diff_count, diff_count_by_subnetwork
