from typing import Any, Dict, List

from enm_api.services.rnc_rbsid.enm_cli import EnmCli
from enm_api.services.rnc_rbsid.parser import parse_rbsid

ENM_SERVERS = ('ENM_SERVER_2', 'ENM_SERVER_4')


def get_rnc_rbsid(siteid: str) -> List[Dict[str, Any]]:
    """Get all rbsIds for matched IubLink."""
    for enm_server in ENM_SERVERS:
        enm_cli = EnmCli(enm_server)
        enm_rbsid_data = enm_cli.get_rnc_rbsid(siteid)
    return parse_rbsid(enm_rbsid_data)
