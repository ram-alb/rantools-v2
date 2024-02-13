from typing import NamedTuple


class RncMo(NamedTuple):
    """A class representing information about an RNC."""

    rnc: str
    ext_gsm_network_id: str


class ExternalGsmCell(NamedTuple):
    """A class representing an external GSM cell."""

    gsm_cell: str
    bcc: int
    band_indicator: str
    external_gsm_cell_id: str
    max_txpower_ul: int
    cell_identity: int
    qrxlev_min: int
    individual_offset: int
    bcch_frequency: int
    lac: int
    ncc: int


def prepare_external_gerancell_config_data(
    neighbor_plan,
    enm_gerancell_data,
    utran_cells,
    ext_gsm_network_ids,
):
    """Prepare data for external geran cells configuration."""
    external_cells = {}

    for pair in neighbor_plan:
        utran_cell = pair.source_cell
        geran_cell = pair.target_cell
        rnc_name = utran_cells[utran_cell]
        ext_gsm_network_id = ext_gsm_network_ids[rnc_name]
        geran_cell_params = enm_gerancell_data[geran_cell]
        external_gsm_cell = ExternalGsmCell(
            gsm_cell=geran_cell,
            bcc=geran_cell_params['bcc'],
            band_indicator=geran_cell_params['band_indicator'],
            external_gsm_cell_id=geran_cell,
            max_txpower_ul=geran_cell_params['max_tx_pwr_ul'],
            cell_identity=geran_cell_params['ci'],
            qrxlev_min=geran_cell_params['qrxlev_min'],
            individual_offset=0,
            bcch_frequency=geran_cell_params['bcchNo'],
            lac=geran_cell_params['lac'],
            ncc=geran_cell_params['ncc'],
        )
        rnc_key = f'{rnc_name}-{ext_gsm_network_id}'
        external_cells.setdefault(rnc_key, set()).add(external_gsm_cell)
    return external_cells


def prepare_gsm_relation_config_data(neighbor_plan, utran_cells, ext_gsm_network_ids):
    """Prepare data for U2G neighbor configuration."""
    gsm_relations = {}
    for pair in neighbor_plan:
        utran_cell = pair.source_cell
        geran_cell = pair.target_cell
        rnc_name = utran_cells[utran_cell]
        ext_gsm_network_id = ext_gsm_network_ids[rnc_name]
        rnc_key = f'{rnc_name}-{ext_gsm_network_id}'
        if rnc_key not in gsm_relations:
            gsm_relations[rnc_key] = {}
        gsm_relation = (rnc_name, ext_gsm_network_id, geran_cell)
        gsm_relations[rnc_key].setdefault(utran_cell, []).append(gsm_relation)
    return gsm_relations
