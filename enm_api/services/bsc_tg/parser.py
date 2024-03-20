from typing import Set

from enmscripting import ElementGroup  # type: ignore


def parse_tg(enm_tg_data: ElementGroup) -> Set[int]:
    """Parse TG data from ENM data."""
    tg_set = set()
    for row in enm_tg_data:
        row_value = row.value()
        if 'FDN' in row_value:
            tg_id = row_value.split('=')[-1]
            tg_set.add(int(tg_id))
    return tg_set
