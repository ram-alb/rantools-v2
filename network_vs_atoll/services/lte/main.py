from network_vs_atoll.services.compare import compare_network_vs_atoll
from network_vs_atoll.services.lte import sql
from network_vs_atoll.services.lte.atoll_handler import handle_atoll_data
from network_vs_atoll.services.select import select_db_data


def main():
    """Compare LTE network data with LTE Atoll data."""
    network_data = select_db_data(sql.NETWORK_QUERY, sql.NetworkRow)
    atoll_data = select_db_data(sql.ATOLL_QUERY, sql.AtollRow)
    atoll_params = handle_atoll_data(atoll_data)

    diffs = {}

    for row in network_data:
        network_params = row._asdict()
        subnetwork = network_params.pop('subnetwork', None)
        atoll_cell_params = atoll_params.get(network_params['cell'], None)
        diff = compare_network_vs_atoll(network_params, atoll_cell_params, technology='LTE')
        if diff:
            diffs.setdefault(subnetwork, []).extend(diff)

    diff_count_by_subnetwork = dict(sorted(
        ((subnetwork, len(diff)) for subnetwork, diff in diffs.items()),
        key=lambda subnetwork_diff: subnetwork_diff[0],
    ))
    total_diff_count = sum(diff_count_by_subnetwork.values())

    return total_diff_count, diff_count_by_subnetwork, diffs
