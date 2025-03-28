from typing import Dict, Optional

from enm_cli import cmedit_get  # type: ignore
from enmscripting import ElementGroup  # type: ignore

ENMS = ("ENM_2", "ENM_4")


def get_enm_sts_data(site: Optional[str] = None) -> Dict[str, ElementGroup]:
    """Get RadioEquipmentClockReference synchronization type and status from ENMs."""
    scope = "*" if site is None else f"*{site.strip()}*"
    cli_command = (
        f"cmedit get {scope} --scopefilter (NetworkElement.neType==RadioNode AND "
        "CmFunction.syncStatus==SYNCHRONIZED AND "
        'networkelement.radioAccessTechnology~~["4G" || "5G"]) '
        "RadioEquipmentClockReference.(syncRefType, referenceStatus) -t"
    )
    return {enm: cmedit_get(enm, cli_command) for enm in ENMS}
