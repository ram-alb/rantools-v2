from typing import List, Tuple

from enm_api.services.bsc_tg.enm_cli import EnmCli
from enm_api.services.bsc_tg.parser import parse_tg

ENM_SERVERS = ('ENM_SERVER_2', 'ENM_SERVER_4')


def get_bsc_tg(bsc_name: str) -> Tuple[List[int], List[int]]:
    """Get all TGs for a given BSC."""
    g12tg = set()
    g31tg = set()

    for enm_server in ENM_SERVERS:
        enm_cli = EnmCli(enm_server)
        enm_g12tg_data = enm_cli.get_bsc_tg(bsc_name, 'G12')
        enm_g31tg_data = enm_cli.get_bsc_tg(bsc_name, 'G31')

        g12tg.update(parse_tg(enm_g12tg_data))
        g31tg.update(parse_tg(enm_g31tg_data))

    return sorted(g12tg), sorted(g31tg)
