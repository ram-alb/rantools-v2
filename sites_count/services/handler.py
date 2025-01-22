from typing import List, NamedTuple


def get_header(field_name: str) -> str:
    """Get header from the field_name of namedtuple."""
    if '_total' in field_name:
        header = field_name.replace('_total', '').capitalize()
    else:
        header = 'Total'
    return header


def handle_selected_data(selected_data: NamedTuple) -> List:
    """Handle selected data from the db."""
    selected_data_dict = selected_data._asdict()

    filtered_selected_data = {
        field: selected_data_dict[field] for field in selected_data_dict.keys()
        if 'created_at' not in field and 'iot' not in field
    }

    sites_data = []

    for field, field_val in filtered_selected_data.items():
        if 'total' in field:
            header = get_header(field)
            total = field_val
            row = []
        elif 'nr5g' in field:
            row.append(field_val)
            sites_data.append([header, *row, total])
        elif 'zte_wcdma' in field:
            row.append(field_val)
            sites_data.append([header, *row, 0, 0, total])
        else:
            row.append(field_val)

    return sorted(sites_data)
