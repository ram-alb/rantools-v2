import functools
import operator
from typing import Dict, List, Tuple

from django.db.models import Count, Max
from django.db.models import Q as MODELSQ
from enm_cli.parser import extract_row_values, get_table  # type: ignore
from enmscripting import ElementGroup  # type: ignore

from tr_data.models import RadioEquipmentClockReference


def _process_enm_sts_data(
    enm_sts_data: Dict[str, ElementGroup],
) -> List[RadioEquipmentClockReference]:
    columns_to_parse = [
        "NodeId",
        "RadioEquipmentClockReferenceId",
        "referenceStatus",
        "syncRefType",
    ]
    sts_rows = []

    for enm, enm_data in enm_sts_data.items():
        table = get_table(enm_data)
        for row in table:
            row_values = extract_row_values(row, *columns_to_parse)
            if None in row_values:
                continue
            node_id, ref_id, ref_status, sync_ref_type = row_values
            sts_rows.append(
                RadioEquipmentClockReference(
                    enm=enm,
                    node_id=node_id,
                    radio_equipment_clock_reference_id=ref_id,
                    reference_status=ref_status,
                    sync_ref_type=sync_ref_type,
                ),
            )

    return sts_rows


def update_sts_data(enm_sts_data: Dict[str, ElementGroup]) -> None:
    """Update RadioEquipmentClockReference data in db while keeping only the latest 4 records."""
    sts_rows = _process_enm_sts_data(enm_sts_data)

    if not sts_rows:
        return

    RadioEquipmentClockReference.objects.bulk_create(sts_rows)

    unique_keys = {
        (row.enm, row.node_id, row.radio_equipment_clock_reference_id)
        for row in sts_rows
    }

    ids_to_keep = set()
    for enm, node_id, ref_id in unique_keys:
        records = RadioEquipmentClockReference.objects.filter(
            enm=enm,
            node_id=node_id,
            radio_equipment_clock_reference_id=ref_id,
        ).order_by(
            "-updated_at",
        )  # От новых к старым
        ids_to_keep.update(records.values_list("id", flat=True)[:4])

    RadioEquipmentClockReference.objects.exclude(id__in=ids_to_keep).delete()


def get_sts_data() -> Tuple[List[str], List[tuple]]:
    """Get RadioEquipmentClockReference data from db."""
    columns_list = [
        field.name
        for field in RadioEquipmentClockReference._meta.fields
        if field.name not in {"id", "updated_at"}
    ]

    fault_keywords = ["PTP_FAULT", "NTP_FAULT", "GNSS_FAULT", "QL_TOO_LOW"]

    fault_records = RadioEquipmentClockReference.objects.filter(
        functools.reduce(
            operator.or_,
            [MODELSQ(reference_status__icontains=kw) for kw in fault_keywords],
        ),
    )

    node_ids_with4_faults = (
        fault_records.values(
            "enm",
            "node_id",
            "radio_equipment_clock_reference_id",
        ).  # Группировка
        annotate(fault_count=Count("id")).  # Подсчитываем количество записей в группе
        filter(fault_count=4).  # Оставляем только те, где их ровно 4
        values_list("node_id", flat=True).  # Достаём node_id
        distinct()  # Убираем дубликаты
    )

    latest_records_subquery = (
        RadioEquipmentClockReference.objects.filter(node_id__in=node_ids_with4_faults).
        values("enm", "node_id", "radio_equipment_clock_reference_id").
        annotate(latest_updated_at=Max("updated_at"))  # Берём максимальный updated_at
    )

    latest_records = RadioEquipmentClockReference.objects.filter(
        node_id__in=[entry["node_id"] for entry in latest_records_subquery],
        updated_at__in=[
            entry["latest_updated_at"] for entry in latest_records_subquery
        ],
    )

    sts_data = list(
        latest_records.order_by(
            "node_id",
            "radio_equipment_clock_reference_id",
        ).values_list(*columns_list),
    )

    return columns_list, sts_data
