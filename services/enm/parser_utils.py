import enum
import re
from typing import List


class MoNames(enum.Enum):
    """Enumeration representing a set of Management Object (MO) names."""

    me_context = 'MeContext'
    managed_element = 'ManagedElement'
    utran_cell = 'UtranCell'
    geran_cell = 'GeranCell'
    ext_gsm_network = 'ExternalGsmNetwork'


def parse_mo_value_from_fdn(fdn: str, mo_type: str) -> str:
    """Parse MO value from FDN string."""
    re_patterns = {
        'SubNetwork': ',SubNetwork=[^,]*',
        'MeContext': 'MeContext=[^,]*',
        'ManagedElement': 'ManagedElement=[^,]*',
        'NRSectorCarrier': 'NRSectorCarrier=.*',
        'NRCellDU': 'NRCellDU=.*',
        'EUtranCellFDD': 'EUtranCellFDD=[A-Za-z0-9-]+',
        'IubLink': 'IubLink=.*',
        'UtranCell': 'UtranCell=.*',
        'GsmSector': 'GsmSector=.*',
        'GeranCell': 'GeranCell=[^,]*',
        'ChannelGroupCell': 'GeranCell=[^,]*',
        'ExternalGsmNetwork': 'ExternalGsmNetwork=.*',
    }

    mo_value_index = -1
    mo_obj = re.search(re_patterns[mo_type], fdn)

    if mo_obj is None:
        raise AttributeError('MO was not found in FDN')

    mo = mo_obj.group()
    return mo.split('=')[mo_value_index]


def parse_ref_parameter(needed_parameter_name: str, ref_value: str) -> List[str]:
    """Parse a parameter name and value from the parameters reference string."""
    all_ref_params = ref_value.split(',')
    name_val_pair = list(filter(
        lambda pair: needed_parameter_name in pair,
        all_ref_params,
    ))[0]
    return name_val_pair.split('=')
