from typing import Dict

from enmscripting import ElementGroup  # type: ignore

from services.enm.parser_utils import MoNames, parse_mo_value_from_fdn, parse_ref_parameter

DELIMETER = ' : '

NodeParams = Dict[str, str]


def parse_rnc_function_params(enm_data: ElementGroup, last_parameter: str) -> Dict[str, NodeParams]:
    """Parse rnc level parameters from ENM data."""
    rnc_parameters = {}
    for row in enm_data:
        row_value = row.value()
        if 'FDN' in row_value:
            rnc_name = parse_mo_value_from_fdn(row_value, MoNames.me_context.value)
            rnc = {}
        elif DELIMETER in row_value:
            parameter_name, parameter_value = row_value.split(DELIMETER)
            if parameter_name == 'mnc' and len(parameter_value) == 1:
                parameter_value = f'0{parameter_value}'
            rnc[parameter_name] = parameter_value
            if parameter_name == last_parameter:
                rnc_parameters[rnc_name] = rnc
    return rnc_parameters


def parse_utran_cell_params(enm_data: ElementGroup, last_parameter: str) -> Dict[str, NodeParams]:
    """Parse utran cell parameters from ENM data."""
    cell_parameters = {}
    for row in enm_data:
        row_value = row.value()
        if 'FDN' in row_value:
            rnc_name = parse_mo_value_from_fdn(row_value, MoNames.me_context.value)
            cell_name = parse_mo_value_from_fdn(row_value, MoNames.utran_cell.value)
            cell = {'rnc': rnc_name}
        elif DELIMETER in row_value:
            parameter_name, parameter_value = row_value.split(DELIMETER)
            if parameter_name == 'locationAreaRef':
                parameter_name, parameter_value = parse_ref_parameter(
                    'LocationArea',
                    parameter_value,
                )
            cell[parameter_name] = parameter_value
            if parameter_name == last_parameter:
                cell_parameters[cell_name] = cell
    return cell_parameters


def parse_geran_cells(enm_data: ElementGroup) -> Dict[str, str]:
    """Parse Geran cell names and BSC names from ENM data."""
    geran_cells = {}
    for row in enm_data:
        row_value = row.value()
        if 'FDN' in row_value:
            bsc_name = parse_mo_value_from_fdn(row_value, MoNames.me_context.value)
            cell_name = parse_mo_value_from_fdn(row_value, MoNames.geran_cell.value)
            geran_cells[cell_name] = bsc_name
    return geran_cells
