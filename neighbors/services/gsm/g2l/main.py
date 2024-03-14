import io

from neighbors.services.date_time import get_date_time
from neighbors.services.excel import get_neighbor_cells_from_excel
from neighbors.services.gsm.g2l.config_preparator import prepare_eutran_frequency_configs
from neighbors.services.network_live.main import split_g2l_neighbors
from neighbors.services.reports.g2l_edff import make_eutran_freq_adding_report

ImportFilePath = str


def generate_g2l_nbr_adding_import_report(g2l_nbr_excel_file: io.BytesIO) -> ImportFilePath:
    """Generate a report for adding G2L neighbors on ENM."""
    planned_neighbors = get_neighbor_cells_from_excel(g2l_nbr_excel_file)

    splitted_neighbors = split_g2l_neighbors(planned_neighbors)

    eutran_freq_configs = prepare_eutran_frequency_configs(
        splitted_neighbors.existing_cells,
        splitted_neighbors.controllers,
    )

    return make_eutran_freq_adding_report(
        eutran_freq_configs,
        splitted_neighbors.non_existing_cells,
        get_date_time(),
    )
