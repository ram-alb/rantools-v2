from typing import Dict, List

from enm_cli.parser import extract_row_values, get_table  # type: ignore
from enmscripting import ElementGroup  # type: ignore


def parse_node_sts_data(enm_data: Dict[str, ElementGroup]) -> List[Dict[str, str]]:
    """Parse synchoronization data for requested Node."""
    node_sts_data = []

    columns_to_parse = [
        'NodeId',
        'RadioEquipmentClockReferenceId',
        'referenceStatus',
        'syncRefType',
    ]

    for enm, sts_data in enm_data.items():
        try:
            table = get_table(sts_data)
        except ValueError:
            continue
        for row in table:
            row_values = extract_row_values(row, *columns_to_parse)
            if None in row_values:
                continue
            sts = dict(zip(columns_to_parse, row_values))
            sts['ENM'] = enm
            node_sts_data.append(sts)

    return sorted(
        node_sts_data,
        key=lambda sts: (sts['NodeId'], sts['RadioEquipmentClockReferenceId']),
    )
