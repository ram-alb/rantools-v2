from typing import Dict

from bts_info.services.enm.cli import EnmCli
from bts_info.services.enm.parser import parse_mimo_types

ENM_SERVERS = ('ENM_SERVER_2', 'ENM_SERVER_4')


def get_mimo_order(site_id: str) -> Dict[str, str]:
    """Get the MIMO order for a given site ID by querying ENM servers."""
    mimo_order = {}
    for enm_server in ENM_SERVERS:
        enm_cli = EnmCli(enm_server)
        enm_tx_data = enm_cli.get_lte_tx_data(site_id)
        if not enm_tx_data.groups():
            continue
        mimo_order.update(parse_mimo_types(enm_tx_data))

    return mimo_order
