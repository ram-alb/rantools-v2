from typing import Dict

from enm_api.services.create_object.enm_cli import EnmCli
from enm_api.services.create_object.utils import get_enm_server


def create_object(object_data: dict) -> Dict[str, str]:
    """Create Base Station object on ENM."""
    # initiate enm instance
    enm_server = get_enm_server(object_data['enm'])
    enm = EnmCli(enm_server)

    # create object
    enm.create_object(object_data)

    # load xml
    if object_data['platform'] == 'COM':
        enm.load_xml(
            sitename=object_data['sitename'],
            enm=object_data['enm'],
        )

    # set BSC/RNC
    if 'GSM' in object_data['technologies']:
        enm.set_controller('GSM', object_data['sitename'], object_data['bsc'])
    if 'UMTS' in object_data['technologies']:
        enm.set_controller('UMTS', object_data['sitename'], object_data['rnc'])

    # return info about new object
    return enm.get_object_info(object_data['sitename'])
