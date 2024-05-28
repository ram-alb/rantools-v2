from typing import List, Tuple

from enm_api.services.create_object.enm_cli import EnmCli
from enm_api.services.create_object.utils import get_enm_server


def create_object(object_data: dict) -> List[Tuple[str, str]]:
    """Create Base Station object on ENM."""
    # initiate enm instance
    enm_server = get_enm_server(object_data['enm'])
    enm = EnmCli(enm_server)
    create_results = []

    # create object
    create_results.extend(enm.create_object(object_data))

    # load xml
    if object_data['platform'] == 'COM':
        load_xml_result = enm.load_xml(
            sitename=object_data['sitename'],
            enm=object_data['enm'],
        )
        create_results.append(load_xml_result)

    # set BSC/RNC
    if 'GSM' in object_data['technologies']:
        create_results.append(
            enm.set_controller('GSM', object_data['sitename'], object_data['bsc']),
        )
    if 'UMTS' in object_data['technologies']:
        create_results.append(
            enm.set_controller('UMTS', object_data['sitename'], object_data['rnc']),
        )

    # return create object results
    return create_results
