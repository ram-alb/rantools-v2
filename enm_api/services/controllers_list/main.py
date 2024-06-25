from typing import Dict, List

from enm_api.services.controllers_list.enm_cli import EnmCli
from enm_api.services.controllers_list.parser import parse_controllers


def get_controllers(enm_pointer: str) -> Dict[str, List[str]]:
    """Retrieve configured BSCs and RNCs from the specified ENM."""
    # initialize enm
    enm = EnmCli(enm_pointer)

    # get ENM data
    enm_data = enm.get_controllers()

    # parse ENM data
    return parse_controllers(enm_data)
