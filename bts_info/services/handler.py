from typing import Any, Dict, List

from bts_info.services.atoll.main import DbData


def append_mimo_order(db_data: DbData, mimo: Dict[str, str]) -> List[Dict[str, Any]]:
    """Process database data and append MIMO order information."""
    handled_data = []

    for selected_data in db_data.values():
        for row in selected_data:
            try:
                mimo_order = mimo[row.cell]
            except KeyError:
                mimo_order = ''

            handled_data.append({**row._asdict(), 'MIMO': mimo_order})

    return handled_data
