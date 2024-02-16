from typing import Dict, List, NamedTuple, Set

from neighbors.services.enm.gsm.parser import NodeParams
from neighbors.services.excel import NeighborPair

MRSL = 30

UtranRelations = Dict[str, List[str]]


class ExternalUtranCell(NamedTuple):
    """A class representing external utran cell params."""

    utran_id: str
    mrsl: int
    scr_code: int
    external_utran_cell_id: str
    fdd_arfcn: int


def _get_utran_id(
    utran_cell: str,
    rnc_params: Dict[str, NodeParams],
    utran_cell_params: Dict[str, NodeParams],
) -> str:
    """Get utranId of utran cell."""
    rnc_name = utran_cell_params[utran_cell]['rnc']
    mcc = rnc_params[rnc_name]['mcc']
    mnc = rnc_params[rnc_name]['mnc']
    lac = utran_cell_params[utran_cell]['LocationArea']
    cell_id = utran_cell_params[utran_cell]['localCellId']
    rnc_id = rnc_params[rnc_name]['rncId']
    return '{mcc}-{mnc}-{lac}-{cell_id}-{rnc_id}'.format(
        mcc=mcc,
        mnc=mnc,
        lac=lac,
        cell_id=cell_id,
        rnc_id=rnc_id,
    )


def prepare_external_ucells_configuration_data(
    neighbor_plan: List[NeighborPair],
    rnc_params: Dict[str, NodeParams],
    utran_cell_params: Dict[str, NodeParams],
    geran_cell_params: Dict[str, str],
) -> Dict[str, Set[ExternalUtranCell]]:
    """Prepare data for external utran cells configuration."""
    external_cells: Dict[str, Set[ExternalUtranCell]] = {}

    for pair in neighbor_plan:
        gsm_cell = pair.source_cell
        utran_cell = pair.target_cell
        bsc_name = geran_cell_params[gsm_cell]
        external_utran_cell = ExternalUtranCell(
            utran_id=_get_utran_id(utran_cell, rnc_params, utran_cell_params),
            mrsl=MRSL,
            scr_code=int(utran_cell_params[utran_cell]['primaryScramblingCode']),
            external_utran_cell_id=utran_cell,
            fdd_arfcn=int(utran_cell_params[utran_cell]['uarfcnDl']),
        )
        external_cells.setdefault(bsc_name, set()).add(external_utran_cell)

    return external_cells


def prepare_g2u_nbr_configuration_data(
    neighbor_plan: List[NeighborPair],
    geran_cell_params: Dict[str, str],
) -> Dict[str, UtranRelations]:
    """Prepare data for G2U neighbor configuration."""
    gu_relations: Dict[str, UtranRelations] = {}
    for pair in neighbor_plan:
        gsm_cell = pair.source_cell
        utran_cell = pair.target_cell
        bsc_name = geran_cell_params[gsm_cell]

        if bsc_name not in gu_relations:
            gu_relations[bsc_name] = {}

        gu_relations[bsc_name].setdefault(gsm_cell, []).append(utran_cell)

    return gu_relations
