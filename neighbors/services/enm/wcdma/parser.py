from typing import Dict

from enmscripting import ElementGroup  # type: ignore

from services.enm.parser_utils import MoNames, parse_mo_value_from_fdn

DELIMETER = ' : '

GerancellParameters = Dict[str, str]


def _get_baseline_params(bcch: str) -> dict:
    max_bcch = 125
    if int(bcch) < max_bcch:
        return {
            'band_indicator': 'OTHER_BANDS',
            'max_tx_pwr_ul': '33',
            'qrxlev_min': '-103',
        }
    return {
        'band_indicator': 'DCS1800',
        'max_tx_pwr_ul': '30',
        'qrxlev_min': '-94',
    }


def parse_gerancell_parameters(
    enm_gerancell_data: ElementGroup,
    last_parameter: str,
) -> Dict[str, GerancellParameters]:
    """Parse necessary gerancells parameters for external geran cells configuration on RNC."""
    gerancell_parameters = {}
    for row in enm_gerancell_data:
        row_value = row.value()
        if 'FDN' in row_value:
            cell_name = parse_mo_value_from_fdn(row_value, MoNames.geran_cell.value)
            cell = {}
        elif DELIMETER in row_value:
            parameter_name, parameter_value = row_value.split(DELIMETER)
            if parameter_name == 'cgi':
                try:
                    _, _, lac, ci = parameter_value.split('-')
                except ValueError:
                    continue
                cell['lac'] = lac
                cell['ci'] = ci
            else:
                cell[parameter_name] = parameter_value
            if parameter_name == last_parameter:
                if 'null' in cell.values():
                    continue
                gerancell_parameters[cell_name] = {**cell, **_get_baseline_params(cell['bcchNo'])}
    return gerancell_parameters


def parse_utran_cells(enm_utrancells_data: ElementGroup) -> Dict[str, str]:
    """Parse utran cell names for each RNC."""
    utran_cells = {}
    for row in enm_utrancells_data:
        row_value = row.value()
        if 'FDN' in row_value:
            rnc_name = parse_mo_value_from_fdn(row_value, MoNames.me_context.value)
            cell_name = parse_mo_value_from_fdn(row_value, MoNames.utran_cell.value)
            utran_cells[cell_name] = rnc_name
    return utran_cells


def parse_external_gsm_network_ids(enm_ext_gsm_network_data: ElementGroup) -> Dict[str, str]:
    """Parse ExternalGsmNetworkId value for each RNC."""
    ext_gsm_network_ids = {}
    for row in enm_ext_gsm_network_data:
        row_value = row.value()
        if 'FDN' in row_value:
            rnc_name = parse_mo_value_from_fdn(row_value, MoNames.me_context.value)
            ext_gsm_network_id = parse_mo_value_from_fdn(row_value, MoNames.ext_gsm_network.value)
            ext_gsm_network_ids[rnc_name] = ext_gsm_network_id
    return ext_gsm_network_ids
