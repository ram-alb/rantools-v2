from datetime import datetime

from neighbors.services.enm import get_enm_g2u_data
from neighbors.services.excel import get_neighbor_cells_from_excel
from neighbors.services.gsm.g2u.create_neighbors import (
    prepare_external_ucells_configuration_data,
    prepare_g2u_nbr_configuration_data,
)
from neighbors.services.network_live import categorize_g2u_neighbors
from neighbors.services.reports import create_g2u_nbr_report


def get_date_time():
    """Get current date and time."""
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]


def generate_g2u_nbr_addition_report(g2u_neighbors_excel_file):
    """Generate a report for the addition of G2U neighbors in ENM."""
    date_time = get_date_time()

    # get planned neighbors from users excel
    planned_neighbors = get_neighbor_cells_from_excel(g2u_neighbors_excel_file)

    # filter planned neighbors
    filtered_neighbors, nonexistent_cells = categorize_g2u_neighbors(planned_neighbors)

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
