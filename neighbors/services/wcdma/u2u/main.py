import io

from neighbors.services.date_time import get_date_time
from neighbors.services.enm.u2u.u2u import get_u2u_enm_data
from neighbors.services.excel import get_neighbor_cells_from_excel
from neighbors.services.network_live.main import split_u2u_neighbors
from neighbors.services.reports.u2u_edff import make_u2u_nbr_adding_report
from neighbors.services.wcdma.u2u.config_preparator import (
    prepare_relations,
    prepare_utran_external_cells,
)

ImportFilePath = str


def generate_u2u_nbr_adding_import_report(u2u_nbr_template: io.BytesIO, enm: str) -> ImportFilePath:
    """Generate a report for the addition of U2U neighbors in ENM."""
    date_time = get_date_time()

    planned_neighbors = get_neighbor_cells_from_excel(u2u_nbr_template)

    splitted_neighbors = split_u2u_neighbors(planned_neighbors, enm)

    enm_utran_cells = get_u2u_enm_data(splitted_neighbors.controllers, enm)

    external_utran_cells_config = prepare_utran_external_cells(
        splitted_neighbors.inter_controllers_neighbors,
        enm_utran_cells,
    )
    inter_rnc_relations_config = prepare_relations(
        splitted_neighbors.inter_controllers_neighbors,
        enm_utran_cells,
    )
    intra_rnc_relations_config = prepare_relations(
        splitted_neighbors.intra_controller_neighbors,
        enm_utran_cells,
    )

    return make_u2u_nbr_adding_report(
        external_utran_cells_config,
        inter_rnc_relations_config,
        intra_rnc_relations_config,
        splitted_neighbors.non_existing_cells,
        date_time,
    )
