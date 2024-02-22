import os
from typing import Dict, List

from neighbors.services.excel import NeighborPair
from neighbors.services.reports.archive import create_zip_archive
from neighbors.services.reports.nonexistent_cells import make_nonexistent_cells_report


def make_external_gerancells_edff(external_gerancells_config: List[Dict[str, str]]) -> List[str]:
    """Create an EDFF part for configuring external geran cells."""
    ext_gerancells = []
    for ext_geran_cell in external_gerancells_config:
        bsc = ext_geran_cell['bsc']
        cell = ext_geran_cell['cell']
        ext_geran_cell_rows = ['create']
        fdn = (
            f'FDN : "SubNetwork=BSC,MeContext={bsc},ManagedElement={bsc},BscFunction=1,BscM=1,'
            f'ExternalGeranCellM=1,ExternalGeranCell={cell}"'
        )
        ext_geran_cell_rows.append(fdn)
        ext_geran_cell_rows.append(f'externalGeranCellId : {cell}')
        ext_geran_cell_params = [
            f'{param_name} : {param_value}' for param_name, param_value in ext_geran_cell.items()
            if param_name not in {'bsc', 'cell'}
        ]
        ext_geran_cell_rows.extend(ext_geran_cell_params)
        ext_gerancells.append('\n'.join(ext_geran_cell_rows))

    return ext_gerancells


def make_g2g_nbr_adding_edff_file(
    external_cells_config: List[str],
    date_time: str,
) -> str:
    """Create a EDFF import file for G2G nbr adding."""
    import_file_path = f'neighbors/reports/G2G_nbr_create_{date_time}.txt'
    external_cells = make_external_gerancells_edff(external_cells_config)
    with open(import_file_path, 'w') as import_file:
        for ext_cell in external_cells:
            import_file.write(ext_cell + '\n')
    return import_file_path


def make_g2g_nbr_adding_report(
    external_cells: List[str],
    non_existing_cells: List[NeighborPair],
    date_time: str,
) -> str:
    """Create a zip file with EDFF for G2G nbr adding and Excel with nonexistent cells."""
    import_file_path = make_g2g_nbr_adding_edff_file(external_cells, date_time)
    non_existing_cells_file_path = make_nonexistent_cells_report(non_existing_cells, date_time)
    g2g_nbr_adding_zip_path = create_zip_archive(
        import_file_path,
        non_existing_cells_file_path,
        date_time,
    )

    os.remove(import_file_path)
    os.remove(non_existing_cells_file_path)

    return g2g_nbr_adding_zip_path
