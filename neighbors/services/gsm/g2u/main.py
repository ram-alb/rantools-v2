import io

from neighbors.services.date_time import get_date_time
from neighbors.services.enm import get_enm_g2u_data
from neighbors.services.excel import get_neighbor_cells_from_excel
from neighbors.services.gsm.g2u.config_preparator import (
    prepare_external_ucells_configuration_data,
    prepare_g2u_nbr_configuration_data,
)
from neighbors.services.network_live import split_gu_neighbors
from neighbors.services.reports import create_g2u_nbr_report

ImportFilePath = str


def generate_g2u_nbr_adding_import_report(
    g2u_neighbors_excel_file: io.BytesIO,
) -> ImportFilePath:
    """Generate a report for the addition of G2U neighbors in ENM."""
    date_time = get_date_time()

    # get planned neighbors from users excel
    planned_neighbors = get_neighbor_cells_from_excel(g2u_neighbors_excel_file)

    # filter planned neighbors
    filtered_neighbors, nonexistent_cells = split_gu_neighbors(planned_neighbors, 'G2U')

    # get data from enm for planned cells
    enm_data = get_enm_g2u_data()

    # create utran external cells
    external_utran_cells = prepare_external_ucells_configuration_data(
        filtered_neighbors,
        enm_data.rnc_params,
        enm_data.utran_cell_params,
        enm_data.geran_cells,
    )

    # create g2u relations
    g2u_relations = prepare_g2u_nbr_configuration_data(filtered_neighbors, enm_data.geran_cells)

    # make xml report for g2u neighbors adding
    return create_g2u_nbr_report(
        external_utran_cells,
        g2u_relations,
        nonexistent_cells,
        date_time,
    )
