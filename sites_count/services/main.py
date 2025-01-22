from datetime import date
from typing import List

from sites_count.services.handler import handle_selected_data
from sites_count.services.select_by_operators import select_by_operators
from sites_count.services.select_by_regions import select_by_regions
from sites_count.services.select_by_vendors import select_by_vendors


def get_site_data(table_type: str, requested_date: date) -> List:
    """Retrieve site data based on the table type and optional requested date."""
    select_funcs = {
        'operator': select_by_operators,
        'vendor': select_by_vendors,
        'region': select_by_regions,
    }

    selected_data = select_funcs[table_type](requested_date)

    return handle_selected_data(selected_data[0])
