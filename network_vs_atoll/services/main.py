from collections import OrderedDict

from network_vs_atoll.services.lte.lte_main import lte_main


def order_diff(diff):
    """
    Order diff dict.

    Args:
        diff (dict): keys - node names, values - list of dicts with cell diffs

    Returns:
        dict: ordered diff, total key moved to the end
    """
    ordered_diff = OrderedDict(sorted(diff.items()))
    ordered_diff.move_to_end('Total')
    return ordered_diff


def main():
    """
    Preapre diff between network and atoll for all technologies.

    Returns:
        tuple: first item is all diffs, second - devided by nodes
    """
    deltas = {
        # 'GSM': order_diff(gsm_main()),
        # 'WCDMA': order_diff(wcdma_main()),
        'LTE': order_diff(lte_main()),
        # 'NR': order_diff(nr_main()),
    }

    deltas_by_nodes = []

    for tech, diffs in deltas.items():
        diff_by_nodes = {
            node: len(diff) for node, diff in diffs.items()
        }
        deltas_by_nodes.append(
            {'technology': tech, 'diffs': diff_by_nodes},
        )

    return (deltas, deltas_by_nodes)
