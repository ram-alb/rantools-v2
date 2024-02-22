import io

from neighbors.services.date_time import get_date_time
from neighbors.services.enm.g2g import get_enm_g2g_data
from neighbors.services.excel import get_neighbor_cells_from_excel
from neighbors.services.gsm.g2g.config_preparator import prepare_geran_external_cells
from neighbors.services.gsm.g2g.split_neighbors import split_neighbors_by_bsc
from neighbors.services.network_live import split_gu_neighbors
from neighbors.services.reports.g2g_edff import make_g2g_nbr_adding_report

ImportFilePath = str


def generate_g2g_nbr_adding_import_report(g2g_nbr_excel_file: io.BytesIO) -> ImportFilePath:
    """Generate a report for the addition of G2G neighbors on ENM."""
    planned_neighbors = get_neighbor_cells_from_excel(g2g_nbr_excel_file)

    existing_cells, non_existing_cells = split_gu_neighbors(planned_neighbors, 'G2G')

    enm_data = get_enm_g2g_data()

    splitted_neighbors = split_neighbors_by_bsc(existing_cells, enm_data.geran_cells)

    external_gerancells_config = prepare_geran_external_cells(
        splitted_neighbors.inter_bsc_neighbors,
        enm_data.geran_cells,
        enm_data.power_control_dl,
        enm_data.power_control_ul,
        enm_data.hierarchical_cell_structure,
    )

    return make_g2g_nbr_adding_report(
        external_gerancells_config,
        non_existing_cells,
        get_date_time(),
    )
