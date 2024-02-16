import os
from typing import Dict, List, Set

from neighbors.services.excel import NeighborPair
from neighbors.services.reports.archive import create_zip_archive
from neighbors.services.reports.nonexistent_cells import make_nonexistent_cells_report
from neighbors.services.reports.u2g_xml import make_u2g_nbr_adding_xml
from neighbors.services.wcdma.u2g.config_preparator import ExternalGsmCell, GsmRelations


def create_u2g_nbr_report(
    ext_geran_cells: Dict[str, Set[ExternalGsmCell]],
    geran_relations: Dict[str, GsmRelations],
    nonexistent_cells: List[NeighborPair],
    date_time: str,
) -> str:
    """Create a zip file with XML for G2U nbr adding and Excel with nonexistent cells."""
    u2g_adding_xml_path = make_u2g_nbr_adding_xml(ext_geran_cells, geran_relations, date_time)
    nonexistent_cells_report_path = make_nonexistent_cells_report(nonexistent_cells, date_time)
    g2u_nbr_zip_path = create_zip_archive(
        u2g_adding_xml_path,
        nonexistent_cells_report_path,
        date_time,
    )
    os.remove(u2g_adding_xml_path)
    os.remove(nonexistent_cells_report_path)
    return g2u_nbr_zip_path
