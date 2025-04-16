from typing import Dict

from enm_cli import cmedit_get, cmedit_get_many  # type: ignore
from enmscripting import ElementGroup  # type: ignore

ENMS = ("ENM_2", "ENM_4")

SCOPE_FILTER = (
    "--scopefilter (NetworkElement.neType==RadioNode AND "
    "CmFunction.syncStatus==SYNCHRONIZED AND "
    'networkelement.radioAccessTechnology~~["4G" || "5G"])'
)


def get_enm_sts_data() -> Dict[str, ElementGroup]:
    """Get RadioEquipmentClockReference synchronization type and status from ENMs."""
    cli_command = (
        f"cmedit get * {SCOPE_FILTER} "
        "RadioEquipmentClockReference.(syncRefType, referenceStatus) -t"
    )
    return {enm: cmedit_get(enm, cli_command) for enm in ENMS}


def get_enm_sts_live_data(site: str):
    """Get sts data for one Node from ENM."""
    scope = f'*{site.strip()}*'
    cli_commands = {
        'PtpBcOcPort': f'cmedit get {scope} {SCOPE_FILTER} PtpBcOcPort.associatedGrandmaster -t',
        'BoundaryOrdinaryClock': (
            f'cmedit get {scope} {SCOPE_FILTER} '
            'BoundaryOrdinaryClock.(ptpProfile, reservedBy) -t'
        ),
        'RadioEquipmentClockReference': (
            f'cmedit get {scope} {SCOPE_FILTER} '
            'RadioEquipmentClockReference.(syncRefType, referenceStatus) -t'
        ),
    }

    return {enm: cmedit_get_many(enm, cli_commands) for enm in ENMS}
