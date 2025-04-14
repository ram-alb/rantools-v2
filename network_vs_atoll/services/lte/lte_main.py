from network_vs_atoll.services.compare import compare
from network_vs_atoll.services.handler import handle_diffs
from network_vs_atoll.services.lte.atoll_handler import (
    get_cell_atoll_params,
    handle_atoll_lte_params,
)
from network_vs_atoll.services.lte.lte_select import (
    select_atoll_params,
    select_network_params,
)
from network_vs_atoll.services.lte.network_handler import get_network_cell_params


def lte_main():
    """
    Compare LTE network and atoll parameters.

    Returns:
        dict: keys - subnetworks, values - list of dicts with cell diffs
    """
    selected_network_params = select_network_params()

    selected_atoll_params = select_atoll_params()
    atoll_params = handle_atoll_lte_params(selected_atoll_params)

    diffs = compare(
        'LTE',
        selected_network_params,
        get_network_cell_params,
        atoll_params,
        get_cell_atoll_params,
    )

    return handle_diffs('subnetwork', diffs)
