from typing import Dict

from neighbors.services.enm.g2g.enm_cli import EnmData
from services.enm.parser_utils import MoNames, parse_mo_value_from_fdn

DELIMETER = ' : '

NodeParams = Dict[str, str]


def parse_enm_data(enm_data: EnmData) -> Dict[str, NodeParams]:
    """Parse parameters from EnmData."""
    enm_params = {}
    for row in enm_data.cmd_output:
        row_value = row.value()
        if 'FDN' in row_value:
            cell_name = parse_mo_value_from_fdn(row_value, MoNames.geran_cell.value)
            bsc_name = parse_mo_value_from_fdn(row_value, MoNames.me_context.value)
            cell = {'bsc': bsc_name}
        elif DELIMETER in row_value:
            parameter_name, parameter_value = row_value.split(DELIMETER)
            cell[parameter_name] = parameter_value
            if parameter_name == enm_data.last_parameter:
                enm_params[cell_name] = cell
    return enm_params
