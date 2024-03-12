import os
from typing import Dict, List

from neighbors.services.excel import NeighborPair
from neighbors.services.reports.archive import create_zip_archive
from neighbors.services.reports.nonexistent_cells import make_nonexistent_cells_report


def _make_external_utrancells_edff(external_utran_cells_config: List[Dict[str, str]]) -> List[str]:
    """Create an EDFF part for configuring ExternalUtranCells."""
    ext_utran_cells = []
    for ext_utran_cell in external_utran_cells_config:
        source_rnc = ext_utran_cell['source_rnc']
        target_rnc = ext_utran_cell['rnc']
        cell = ext_utran_cell['cell']
        ext_utran_cell_rows = ['create']
        fdn = (
            f'FDN : "SubNetwork=RNC,MeContext={source_rnc},ManagedElement=1,RncFunction=1,'
            f'IurLink={target_rnc},ExternalUtranCell={cell}"'
        )
        ext_utran_cell_rows.append(fdn)

        ext_utran_cell_params = [
            f'{param_name} : {param_value}' for param_name, param_value in ext_utran_cell.items()
            if param_name not in {'rnc', 'LocationArea', 'RoutingArea', 'source_rnc', 'cell'}
        ]

        ext_utran_cell_rows.extend(ext_utran_cell_params)
        ext_utran_cell_rows.append(
            f'lac : {ext_utran_cell["LocationArea"]}',
        )
        ext_utran_cell_rows.append(
            f'rac : {ext_utran_cell["RoutingArea"]}',
        )
        ext_utran_cell_rows.append(
            f'ExternalUtranCellId : {cell}',
        )
        ext_utran_cell_rows.append(
            f'userLabel : {cell}',
        )
        ext_utran_cell_rows.append(
            'cellCapability : {cpcSupport=ON, edchSupport=ON, edchTti2CmSupport=OFF, '
            'edchTti2Support=ON, enhancedL2Support=ON, fdpchSupport=ON, hsdschSupport=ON, '
            'multiCarrierSupport=OFF, qam64MimoSupport=OFF}',
        )
        ext_utran_cells.append('\n'.join(ext_utran_cell_rows))
    return ext_utran_cells


def _make_utran_relations_edff(
    inter_rnc_relations_config: List[Dict[str, str]],
    relation_type: str,
) -> List[str]:
    """Create an EDFF part for configuring inter RNC UtranRelations."""
    utran_relations = []
    for relation in inter_rnc_relations_config:
        source_cell = relation['source_cell']
        target_cell = relation['target_cell']
        source_rnc = relation['source_rnc']

        relation_rows = ['create']

        fdn = (
            f'FDN : "SubNetwork=RNC,MeContext={source_rnc},ManagedElement=1,RncFunction=1,'
            f'UtranCell={source_cell},UtranRelation={target_cell}"'
        )
        relation_rows.append(fdn)

        relation_rows.append(f'UtranRelationId : {target_cell}')
        if relation_type == 'inter_rnc':
            relation_rows.append(
                f'utranCellRef : "SubNetwork=RNC,MeContext={source_rnc},ManagedElement=1,'
                f'RncFunction=1,IurLink={relation["target_rnc"]},ExternalUtranCell={target_cell}"',
            )
        elif relation_type == 'intra_rnc':
            relation_rows.append(
                f'utranCellRef : "SubNetwork=RNC,MeContext={source_rnc},ManagedElement=1,'
                f'RncFunction=1,UtranCell={target_cell}"',
            )

        utran_relations.append('\n'.join(relation_rows))
    return utran_relations


def _make_u2u_nbr_adding_edff_file(
    external_utran_cells_config: List[Dict[str, str]],
    inter_rnc_relations_config: List[Dict[str, str]],
    intra_rnc_realtions_config: List[Dict[str, str]],
    date_time: str,
) -> str:
    """Create a EDFF import file for U2U nbr adding."""
    import_file_path = f'neighbors/reports/U2U_nbr_create_{date_time}.txt'
    external_utran_cells = _make_external_utrancells_edff(external_utran_cells_config)
    inter_rnc_relatins = _make_utran_relations_edff(inter_rnc_relations_config, 'inter_rnc')
    intra_rnc_relatins = _make_utran_relations_edff(intra_rnc_realtions_config, 'intra_rnc')
    with open(import_file_path, 'w') as import_file:
        for ext_cell in external_utran_cells:
            import_file.write(ext_cell + '\n')
        for inter_rnc_relation in inter_rnc_relatins:
            import_file.write(inter_rnc_relation + '\n')
        for intra_rnc_relation in intra_rnc_relatins:
            import_file.write(intra_rnc_relation + '\n')
    return import_file_path


def make_u2u_nbr_adding_report(
    external_cells: List[Dict[str, str]],
    inter_rnc_relations: List[Dict[str, str]],
    intra_rnc_relations: List[Dict[str, str]],
    non_existing_cells: List[NeighborPair],
    date_time: str,
) -> str:
    """Create a zip file with EDFF for G2G nbr adding and Excel with nonexistent cells."""
    import_file_path = _make_u2u_nbr_adding_edff_file(
        external_cells,
        inter_rnc_relations,
        intra_rnc_relations,
        date_time,
    )

    non_existing_cells_file_path = make_nonexistent_cells_report(non_existing_cells, date_time)

    u2u_nbr_adding_zip_path = create_zip_archive(
        import_file_path,
        non_existing_cells_file_path,
        date_time,
    )

    os.remove(import_file_path)
    os.remove(non_existing_cells_file_path)

    return u2u_nbr_adding_zip_path
