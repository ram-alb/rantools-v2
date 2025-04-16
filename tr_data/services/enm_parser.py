from typing import Dict, List, Optional

from enm_cli.parser import extract_row_values, get_table  # type: ignore
from enmscripting import ElementGroup  # type: ignore


def _parse_ptpbcocport(enm_data: ElementGroup) -> Dict[str, str]:
    grandmaster_data = {}
    columns_to_parse = [
        "NodeId",
        "BoundaryOrdinaryClockId",
        "associatedGrandmaster",
    ]

    for row in get_table(enm_data):
        row_values = extract_row_values(row, *columns_to_parse)
        if None in row_values:
            continue
        node, boundary_clock, grandmaster = row_values
        grandmaster_data[f'{node}:{boundary_clock}'] = grandmaster
    return grandmaster_data


def _parse_radio_equipment_clock_reference(reserved_by: str) -> Optional[str]:
    parts = reserved_by.strip("[]").split(",")
    for part in parts:
        if part.startswith("RadioEquipmentClockReference="):
            return part.split("=")[1]
    return None


def _parse_boundary_ordinary_clock(enm_data: ElementGroup) -> Dict[str, Dict[str, str]]:
    boundary_data = {}
    columns_to_parse = [
        "NodeId",
        "BoundaryOrdinaryClockId",
        "ptpProfile",
        "reservedBy",
    ]
    for row in get_table(enm_data):
        row_values = extract_row_values(row, *columns_to_parse)
        if None in row_values:
            continue
        node, boundary_clock, ptp_profile, reserved_by = row_values
        ref_id = _parse_radio_equipment_clock_reference(reserved_by)
        if ref_id:
            boundary_data[f'{node}:{ref_id}'] = {
                "boundary_clock": boundary_clock,
                "ptp_profile": ptp_profile,
            }
    return boundary_data


def _handle_sts_row(
    row,
    enm: str,
    ordinary_data: Dict[str, Dict[str, str]],
    port_data: Dict[str, str],
) -> Dict[str, Optional[str]]:
    columns_to_parse = [
        "NodeId",
        "RadioEquipmentClockReferenceId",
        "referenceStatus",
        "syncRefType",
    ]
    row_values = extract_row_values(row, *columns_to_parse)
    sts = dict(zip(columns_to_parse, row_values))
    sts["ENM"] = enm

    node, ref_id, _, _ = row_values
    try:
        boundary_clock = ordinary_data[f'{node}:{ref_id}']["boundary_clock"]
        ptp_profile = ordinary_data[f'{node}:{ref_id}']["ptp_profile"]
        grandmaster = port_data[f'{node}:{boundary_clock}']
    except KeyError:
        ptp_profile = None
        grandmaster = None

    sts["ptpProfile"] = ptp_profile
    sts["associatedGrandmaster"] = grandmaster

    return sts


def parse_node_sts_data(enm_data: Dict[str, Dict[str, ElementGroup]]) -> List[Dict[str, str]]:
    """Parse synchoronization data for requested Node."""
    node_sts_data = []

    for enm, sts_data in enm_data.items():
        clock_data = sts_data['RadioEquipmentClockReference']
        try:
            table = get_table(clock_data)
        except ValueError:
            continue

        port_data = _parse_ptpbcocport(sts_data['PtpBcOcPort'])
        ordinary_data = _parse_boundary_ordinary_clock(sts_data['BoundaryOrdinaryClock'])

        for row in table:
            sts = _handle_sts_row(row, enm, ordinary_data, port_data)
            node_sts_data.append(sts)

    return sorted(
        node_sts_data,  # type: ignore
        key=lambda sts: (sts["NodeId"], sts["RadioEquipmentClockReferenceId"]),
    )
