from network_vs_atoll.services.compare import aggregate_diffs, calculate_diffs
from network_vs_atoll.services.nr import sql
from network_vs_atoll.services.nr.atoll_handler import handle_atoll_data
from network_vs_atoll.services.select import select_db_data


def main():
    """Compare NR network data with Atoll data."""
    network_data = select_db_data(sql.NETWORK_QUERY, sql.NetworkRow)
    atoll_data = select_db_data(sql.ATOLL_QUERY, sql.AtollRow)
    atoll_params = handle_atoll_data(atoll_data)

    diffs = calculate_diffs(network_data, atoll_params)

    total_diff_count, diff_count_by_subnetwork = aggregate_diffs(diffs)

    return total_diff_count, diff_count_by_subnetwork, diffs
