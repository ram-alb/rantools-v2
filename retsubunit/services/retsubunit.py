from typing import Dict, List, Optional

from retsubunit.services.enm import get_enm_retsubunit_data, retsubunit_params
from retsubunit.services.parser import parse_retsubunit_data


def get_retsubunits(site: Optional[str] = None) -> List[Dict[str, str]]:
    """Get RetSubUnit data from ENM and parse it."""
    enm_data = get_enm_retsubunit_data(site)
    return parse_retsubunit_data(enm_data, retsubunit_params)
