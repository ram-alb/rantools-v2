from typing import NamedTuple

from services.enm.parser_utils import MoNames, parse_mo_value_from_fdn, parse_ref_parameter

DELIMETER = ' : '


def _convert_to_int_or_keep(parameter_value):
    try:
        return int(parameter_value)
    except ValueError:
        return parameter_value


def _get_baseline_params(bcch):
    if bcch < 125:
        return {
            'band_indicator': 'OTHER_BANDS',
            'max_tx_pwr_ul': 33,
            'qrxlev_min': -103,
        }
    return {
        'band_indicator': 'DCS1800',
        'max_tx_pwr_ul': 30,
        'qrxlev_min': -94,
    }


def parse_gerancell_parameters(enm_gerancell_data, last_parameter):
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
                cell['lac'] = _convert_to_int_or_keep(lac)
                cell['ci'] = _convert_to_int_or_keep(ci)
            else:
                cell[parameter_name] = _convert_to_int_or_keep(parameter_value)
            if parameter_name == last_parameter:
                if 'null' in cell.values():
                    continue
                gerancell_parameters[cell_name] = {**cell, **_get_baseline_params(cell['bcchNo'])}
    return gerancell_parameters


def parse_utran_cells(enm_utrancells_data):
    utran_cells = {}
    for row in enm_utrancells_data:
        row_value = row.value()
        if 'FDN' in row_value:
            rnc_name = parse_mo_value_from_fdn(row_value, MoNames.me_context.value)
            cell_name = parse_mo_value_from_fdn(row_value, MoNames.utran_cell.value)
            utran_cells[cell_name] = rnc_name
    return utran_cells


def parse_external_gsm_network_ids(enm_ext_gsm_network_data):
    ext_gsm_network_ids = {}
    for row in enm_ext_gsm_network_data:
        row_value = row.value()
        if 'FDN' in row_value:
            rnc_name = parse_mo_value_from_fdn(row_value, MoNames.me_context.value)
            ext_gsm_network_id = parse_mo_value_from_fdn(row_value, MoNames.ext_gsm_network.value)
            ext_gsm_network_ids[rnc_name] = ext_gsm_network_id
    return ext_gsm_network_ids
