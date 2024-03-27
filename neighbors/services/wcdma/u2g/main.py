import io

from neighbors.services.date_time import get_date_time
from neighbors.services.enm.wcdma import get_enm_u2g_data
from neighbors.services.excel import get_neighbor_cells_from_excel
from neighbors.services.network_live.main import split_gu_neighbors
from neighbors.services.reports.u2g_main import create_u2g_nbr_report
from neighbors.services.wcdma.u2g.config_preparator import (
    prepare_external_gerancell_config_data,
    prepare_gsm_relation_config_data,
)

ImportFilePath = str


def generate_u2g_nbr_adding_import_report(u2g_nbr_template: io.BytesIO, enm: str) -> ImportFilePath:
    """Generate a report for the addition of U2G neighbors in ENM."""
    date_time = get_date_time()

    # get planned neighbors
    planned_neighbors = get_neighbor_cells_from_excel(u2g_nbr_template)

    # split planned neigbors to list of NeighborPairs where cells are exists in NL and not exists
    splitted_neighbors = split_gu_neighbors(planned_neighbors, 'U2G', enm)

    # get data from ENM
    enm_u2g_data = get_enm_u2g_data(
        splitted_neighbors.source_controllers,
        splitted_neighbors.target_controllers,
        enm,
    )

    # generate gsm external cells
    ext_gsm_cells = prepare_external_gerancell_config_data(
        splitted_neighbors.existing_cells,
        enm_u2g_data.geran_cell_params,
        enm_u2g_data.utran_cells,
        enm_u2g_data.ext_gsm_network_ids,
    )

    # generate gsm relations
    gsm_relations = prepare_gsm_relation_config_data(
        splitted_neighbors.existing_cells,
        enm_u2g_data.utran_cells,
        enm_u2g_data.ext_gsm_network_ids,
    )

    # generate xml import file
    return create_u2g_nbr_report(
        ext_gsm_cells,
        gsm_relations,
        splitted_neighbors.non_existing_cells,
        date_time,
    )
