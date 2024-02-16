from typing import Dict, List, NamedTuple, Set, Tuple

from neighbors.services.enm.wcdma.parser import GerancellParameters
from neighbors.services.excel import NeighborPair

GsmRelations = Dict[str, List[Tuple[str, str, str]]]


class RncMo(NamedTuple):
    """A class representing information about an RNC."""

    rnc: str
    ext_gsm_network_id: str


class ExternalGsmCell(NamedTuple):
    """A class representing an external GSM cell."""

    gsm_cell: str
    bcc: str
    band_indicator: str
    external_gsm_cell_id: str
    max_txpower_ul: str
    cell_identity: str
    qrxlev_min: str
    individual_offset: int
    bcch_frequency: str
    lac: str
    ncc: str


def prepare_external_gerancell_config_data(
    neighbor_plan: List[NeighborPair],
    enm_gerancell_data: Dict[str, GerancellParameters],
    utran_cells: Dict[str, str],
    ext_gsm_network_ids: Dict[str, str],
) -> Dict[str, Set[ExternalGsmCell]]:
    """Prepare data for external geran cells configuration."""
    external_cells: Dict[str, Set[ExternalGsmCell]] = {}

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


def prepare_gsm_relation_config_data(
    neighbor_plan: List[NeighborPair],
    utran_cells: Dict[str, str],
    ext_gsm_network_ids: Dict[str, str],
) -> Dict[str, GsmRelations]:
    """Prepare data for U2G neighbor configuration."""
    gsm_relations: Dict[str, GsmRelations] = {}
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
