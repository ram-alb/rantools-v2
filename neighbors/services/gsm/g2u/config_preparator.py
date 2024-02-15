def get_utran_id(utran_cell, rnc_params, utran_cell_params):
    """Get utranId of utran cell."""
    rnc_name = utran_cell_params[utran_cell]['rnc']
    mcc = rnc_params[rnc_name]['mcc']
    mnc = rnc_params[rnc_name]['mnc']
    lac = utran_cell_params[utran_cell]['LocationArea']
    cell_id = utran_cell_params[utran_cell]['localCellId']
    rnc_id = rnc_params[rnc_name]['rncId']
    return '{mcc}-{mnc}-{lac}-{cell_id}-{rnc_id}'.format(
        mcc=mcc,
        mnc=mnc,
        lac=lac,
        cell_id=cell_id,
        rnc_id=rnc_id,
    )


def _filter_external_utran_cells(external_cells):
    """Filter external utran cells from duplicated cells."""
    filtered_external_utran_cells = {}
    for bsc, ext_utran_cells in external_cells.items():
        uniq_ext_cells_items = {tuple(ext_cell.items()) for ext_cell in ext_utran_cells}
        uniq_ext_utran_cells = [
            dict(ext_cell_items) for ext_cell_items in uniq_ext_cells_items
        ]
        filtered_external_utran_cells[bsc] = uniq_ext_utran_cells
    return filtered_external_utran_cells


def prepare_external_ucells_configuration_data(
    neighbor_plan,
    rnc_params,
    utran_cell_params,
    geran_cell_params,
):
    """Prepare data for external utran cells configuration."""
    external_cells = {}

    for pair in neighbor_plan:
        gsm_cell = pair.source_cell
        utran_cell = pair.target_cell
        bsc_name = geran_cell_params[gsm_cell]
        external_utran_cell = {
            'utranId': get_utran_id(utran_cell, rnc_params, utran_cell_params),
            'mrsl': 30,
            'scrCode': utran_cell_params[utran_cell]['primaryScramblingCode'],
            'externalUtranCellId': utran_cell,
            'fddArfcn': utran_cell_params[utran_cell]['uarfcnDl'],
        }
        external_cells.setdefault(bsc_name, []).append(external_utran_cell)

    return _filter_external_utran_cells(external_cells)


def prepare_g2u_nbr_configuration_data(neighbor_plan, geran_cell_params):
    """Prepare data for G2U neighbor configuration."""
    gu_relations = {}
    for pair in neighbor_plan:
        gsm_cell = pair.source_cell
        utran_cell = pair.target_cell
        bsc_name = geran_cell_params[gsm_cell]

        if bsc_name not in gu_relations:
            gu_relations[bsc_name] = {}

        gu_relations[bsc_name].setdefault(gsm_cell, []).append(utran_cell)

    return gu_relations
