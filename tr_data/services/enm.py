from typing import Dict, List, Tuple

from enm_cli import cmedit_get  # type: ignore
from enm_cli.parser import extract_row_values, get_table  # type: ignore
from enmscripting import ElementGroup  # type: ignore


def _get_enm_sts_data() -> Dict[str, ElementGroup]:
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


def _process_enm_sts_data(enm_sts_data: Dict[str, ElementGroup]) -> Tuple[List[str], List[tuple]]:
    columns_to_parse = [
        'NodeId',
        'RadioEquipmentClockReferenceId',
        'referenceStatus',
        'syncRefType',
    ]
    columns = ['ENM', *columns_to_parse]
    sts_data = []

    for enm, enm_data in enm_sts_data.items():
        table = get_table(enm_data)
        for row in table:
            row_values = extract_row_values(row, *columns_to_parse)
            sts_data.append((enm, *row_values))

    return columns, sorted(sts_data)


def get_sts():
    """Get the STS data from the ENMs."""
    enm_sts_data = _get_enm_sts_data()
    return _process_enm_sts_data(enm_sts_data)
