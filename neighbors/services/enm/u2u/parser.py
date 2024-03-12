from typing import Dict, List, Tuple

from enmscripting import ElementGroup  # type: ignore

from services.enm.parser_utils import MoNames, parse_mo_value_from_fdn

DELIMETER = ' : '

NodeParams = Dict[str, str]


def _parse_ref_parameter(ref_parameter: str) -> List[str]:
    """Parse parameter name and value of Reference parameter."""
    ref_parameter_data = ref_parameter.split(',')[-1]
    return ref_parameter_data.split('=')


def parse_utran_cell_params(enm_data: Tuple[ElementGroup, str]) -> Dict[str, NodeParams]:
    """Parse UtranCell parameters from ENM data."""
    utran_cell_params = {}
    utran_cell_data, last_parameter = enm_data
    for row in utran_cell_data:
        row_value = row.value()
        if 'FDN' in row_value:
            cell_name = parse_mo_value_from_fdn(row_value, MoNames.utran_cell.value)
            rnc_name = parse_mo_value_from_fdn(row_value, MoNames.me_context.value)
            cell = {'rnc': rnc_name}
        elif DELIMETER in row_value:
            parameter_name, parameter_value = row_value.split(DELIMETER)

            if parameter_name.endswith('Ref'):
                parameter_name, parameter_value = _parse_ref_parameter(parameter_value)
            cell[parameter_name] = parameter_value

            if parameter_name == last_parameter:
                utran_cell_params[cell_name] = cell

    return utran_cell_params
