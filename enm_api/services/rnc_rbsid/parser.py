from typing import Any, Dict, List

from enmscripting import ElementGroup


def parse_rbsid(enm_rbsid_data: ElementGroup) -> List[Dict[str, Any]]:
    """Parse RbsId, IubLink, RNC Name data from ENM data."""
    all_rbsid = []
    iub = ''

    for row in enm_rbsid_data:
        row_value = row.value()
        if 'FDN' in row_value:
            parts = row_value.split('=')
            iub = parts[-1]
            rnc = parts[2].split(',')[0]
            rbsid_dict = {
                'Rnc': rnc,
                'Name': iub,
                'RbsId': '',
            }
        if row_value.startswith('rbsId'):
            rbsid_dict['RbsId'] = row_value.split(':')[-1].strip()
            all_rbsid.append(rbsid_dict)
    return all_rbsid
