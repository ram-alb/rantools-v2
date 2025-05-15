from network_vs_atoll.services.lte.main import main as lte_main
from network_vs_atoll.services.nr.main import main as nr_main


def main() -> dict:
    """Compare network data with Atoll data for different technologies."""
    tech_functions = {
        'LTE': lte_main,
        'NR': nr_main,
    }

    network_vs_atoll_results = {
        'summary': {},
        'summary_by_technologies': {},
        'diffs': {},
    }

    for tech, func in tech_functions.items():
        total_diff_count, diff_count_by_subnetwork, diffs = func()
        network_vs_atoll_results['summary'][tech] = total_diff_count
        network_vs_atoll_results['summary_by_technologies'][tech] = diff_count_by_subnetwork
        network_vs_atoll_results['diffs'][tech] = diffs

    return network_vs_atoll_results
