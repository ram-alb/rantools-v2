from typing import Dict, List

from enm_cli.parser import extract_row_values  # type: ignore
from enmscripting import ElementGroup  # type: ignore


def _get_columns_to_parse(table: ElementGroup, retsubunit_params: List[str]) -> List[str]:
    mo_types1 = [
        "NodeId",
        "AntennaUnitGroupId",
        "AntennaNearUnitId",
    ]

    mo_types2 = [
        "NodeId",
        "FieldReplaceableUnitId",
        "AntennaNearUnitId",
    ]

    table_columns = table.labels()[0]

    if "FieldReplaceableUnit" in table_columns:
        return mo_types2 + retsubunit_params

    return mo_types1 + retsubunit_params


def _process_table(
    enm: str, table: ElementGroup, columns_to_parse: List[str],
) -> List[Dict[str, str]]:
    ret_data = []
    for row in table:
        row_values = extract_row_values(row, *columns_to_parse)
        ret = dict(zip(columns_to_parse, row_values))
        ret["ENM"] = enm
        ret["SectorUnit"] = (
            ret.pop("AntennaUnitGroupId")
            if "AntennaUnitGroupId" in ret
            else ret.pop("FieldReplaceableUnitId")
        )
        ret_data.append(ret)
    return ret_data


def parse_retsubunit_data(
    enm_data: Dict[str, ElementGroup], retsubunit_params=tuple,
) -> List[Dict[str, str]]:
    """Parse the ENM data and extract RetSubUnit information."""
    retsubunit_data = []

    for enm, enm_retsubunit_data in enm_data.items():
        tables = enm_retsubunit_data.groups()
        if not tables:
            continue

        for table in tables:
            columns_to_parse = _get_columns_to_parse(table, retsubunit_params)

            ret_data = _process_table(enm, table, columns_to_parse)
            retsubunit_data.extend(ret_data)

    return sorted(
        retsubunit_data,
        key=lambda ret: (ret["NodeId"], ret["SectorUnit"], ret["AntennaNearUnitId"]),
    )
