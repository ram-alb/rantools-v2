from typing import Dict, List, Tuple

from django.db import connection  # type: ignore
from enm_cli.parser import extract_row_values, get_table  # type: ignore
from enmscripting import ElementGroup  # type: ignore

from tr_data.models import RadioEquipmentClockReference


def _process_enm_sts_data(
    enm_sts_data: Dict[str, ElementGroup],
) -> List[RadioEquipmentClockReference]:
    columns_to_parse = [
        'NodeId',
        'RadioEquipmentClockReferenceId',
        'referenceStatus',
        'syncRefType',
    ]
    sts_rows = []

    for enm, enm_data in enm_sts_data.items():
        table = get_table(enm_data)
        for row in table:
            row_values = extract_row_values(row, *columns_to_parse)
            if None in row_values:
                continue
            node_id, ref_id, ref_status, sync_ref_type = row_values
            sts_rows.append(RadioEquipmentClockReference(
                enm=enm,
                node_id=node_id,
                radio_equipment_clock_reference_id=ref_id,
                reference_status=ref_status,
                sync_ref_type=sync_ref_type,
            ))

    return sts_rows


def update_sts_data(enm_sts_data: Dict[str, ElementGroup]) -> None:
    """Update RadioEquipmentClockReference data in db."""
    sts_rows = _process_enm_sts_data(enm_sts_data)

    if sts_rows:
        with connection.cursor() as cursor:
            if connection.vendor == 'sqlite':
                cursor.execute("DELETE FROM tr_data_radioequipmentclockreference")
                cursor.execute(
                    "DELETE FROM sqlite_sequence WHERE name='tr_data_radioequipmentclockreference'",
                )
            else:
                cursor.execute(
                    "TRUNCATE TABLE tr_data_radioequipmentclockreference RESTART IDENTITY",
                )
        RadioEquipmentClockReference.objects.bulk_create(sts_rows)


def get_sts_data() -> Tuple[List[str], List[tuple]]:
    """Get RadioEquipmentClockReference data from db."""
    columns_list = [
        field.name for field in RadioEquipmentClockReference._meta.fields
        if field.name not in {'id', 'updated_at'}
    ]
    sts_data = list(
        RadioEquipmentClockReference.objects.
        order_by('node_id', 'radio_equipment_clock_reference_id').
        values_list(*columns_list),
    )
    return columns_list, sts_data
