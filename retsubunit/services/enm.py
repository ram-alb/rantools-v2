from typing import Dict, Optional

from enm_cli import cmedit_get  # type: ignore
from enmscripting import ElementGroup  # type: ignore

from services.enm.enmscripting import Enms

retsubunit_params = [
    "electricalAntennaTilt",
    "iuantAntennaModelNumber",
    "iuantAntennaSerialNumber",
    "maxTilt",
    "minTilt",
]


def get_enm_retsubunit_data(site: Optional[str] = None) -> Dict[str, ElementGroup]:
    """Get RetSubUnit data from ENM."""
    scope = "*" if site is None else f"*{site.strip()}*"
    cli_command = "cmedit get {scope} RetSubUnit.({params}) -t".format(
        scope=scope,
        params=",".join(retsubunit_params),
    )

    return {enm.value: cmedit_get(enm.value, cli_command) for enm in Enms}
