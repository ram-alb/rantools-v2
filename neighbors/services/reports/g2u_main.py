import os

from neighbors.services.reports.archive import create_zip_archive
from neighbors.services.reports.g2u_xml import make_g2u_nbr_adding_xml
from neighbors.services.reports.nonexistent_cells import make_nonexistent_cells_report


def create_g2u_nbr_report(external_utran_cells, g2u_relations, nonexistent_cells, date_time):
    """Create a zip file with XML for G2U nbr adding and Excel with nonexistent cells."""
    g2u_adding_xml_path = make_g2u_nbr_adding_xml(external_utran_cells, g2u_relations, date_time)
    nonexistent_cells_report_path = make_nonexistent_cells_report(nonexistent_cells, date_time)
    g2u_nbr_zip_path = create_zip_archive(
        g2u_adding_xml_path,
        nonexistent_cells_report_path,
        date_time,
    )
    os.remove(g2u_adding_xml_path)
    os.remove(nonexistent_cells_report_path)
    return g2u_nbr_zip_path
