from typing import Dict

from enmscripting import ElementGroup  # type: ignore

from services.enm.parser_utils import parse_mo_value_from_fdn


def parse_mimo_types(tx_data: ElementGroup) -> Dict[str, str]:
    """Parse MIMO types from the given tx data."""
    mimo_types = {
        '0': 'no MIMO',
        '1': 'no MIMO',
        '2': 'MIMO 2*2',
        '4': 'MIMO 4*4',
    }

    tx_nums = {}

    table = tx_data.groups()[0]
    for row in table:
        tx_num = row.find_by_label('noOfTxAntennas')[0].value()
        reserved_by = row.find_by_label('reservedBy')[0].value()
        try:
            cell_name = parse_mo_value_from_fdn(reserved_by, 'EUtranCellFDD')
        except AttributeError:
            continue
        tx_nums[cell_name] = mimo_types[tx_num]

    return tx_nums
