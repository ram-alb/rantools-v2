from typing import Dict, List


def get_unique_dicts(
    values_list: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    """Get a list of unique dicts."""
    unique_vals = {tuple(dict_val.items()) for dict_val in values_list}
    return [dict(keys_vals) for keys_vals in unique_vals]
