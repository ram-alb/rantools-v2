from typing import Optional


def get_rach(rach_list: str) -> Optional[int]:
    """Extract the RACH value from a string."""
    if rach_list is None:
        return None
    if rach_list.isnumeric():
        return int(rach_list)

    return int(rach_list.split('-')[0])
