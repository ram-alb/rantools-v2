from typing import Dict

from enm_cli import cmedit_get  # type: ignore
from enmscripting import ElementGroup  # type: ignore


def get_enm_sts_data() -> Dict[str, ElementGroup]:
    """Get RadioEquipmentClockReference synchronization type and status from ENMs."""
    cli_command = (
        'cmedit get * --scopefilter (NetworkElement.neType==RadioNode AND '
        'CmFunction.syncStatus==SYNCHRONIZED AND '
        'networkelement.radioAccessTechnology~~["4G"]) '
        'RadioEquipmentClockReference.(syncRefType, referenceStatus) -t'
    )
    enms = ('ENM_2', 'ENM_4')
    return {
        enm: cmedit_get(enm, cli_command)
        for enm in enms
    }
