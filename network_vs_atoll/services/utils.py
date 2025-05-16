from typing import Dict, Optional, Union

ParameterValue = Union[int, str, None]
CellParams = Dict[str, ParameterValue]
AtollParams = Dict[str, CellParams]


def get_rach(rach_list: Optional[str]) -> ParameterValue:
    """Extract the RACH value from a string."""
    if rach_list is None:
        return None
    if rach_list.isnumeric():
        return int(rach_list)

    try:
        return int(rach_list.split('-')[0])
    except ValueError:
        return rach_list


def handle_cellid(cellid: Optional[str]) -> ParameterValue:
    """
    Convert cellid to int if possible.

    If conversion fails, return the original string for user-visible diff reporting.
    If input is None, return None.
    """
    if cellid is None:
        return None
    try:
        return int(cellid)
    except ValueError:
        return cellid
