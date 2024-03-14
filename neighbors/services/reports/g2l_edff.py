import os
from typing import List

from neighbors.services.excel import NeighborPair
from neighbors.services.gsm.g2l.config_preparator import EUtranFrequency
from neighbors.services.reports.archive import create_zip_archive
from neighbors.services.reports.nonexistent_cells import make_nonexistent_cells_report


def make_eutran_freq_edff(eutran_freq_configs: List[EUtranFrequency]) -> List[str]:
    """Create an EDFF part for configuring EUtranFrequency."""
    eutran_freqs = []
    for config in eutran_freq_configs:
        config_rows = ['create']
        fdn = (
            f'FDN : "SubNetwork=BSC,MeContext={config.bsc},ManagedElement={config.bsc},'
            f'BscFunction=1,BscM=1,GeranCellM=1,GeranCell={config.cell},'
            f'Mobility=1,InterRanMobility=1,EUtranFrequency={config.eutran_frequency}"'
        )
        config_rows.append(fdn)
        config_rows.append(f'eUtranFrequencyId : {config.eutran_frequency}')
        config_rows.append(f'hPrioThrE : {config.h_prio_thr_e}')
        config_rows.append(f'lPrioThrE : {config.l_prio_thr_e}')
        config_rows.append(f'qRxLevMinE : {config.q_rxlev_min_e}')
        config_rows.append(f'ratPrioE : {config.rat_prio_e}')
        eutran_freqs.append(
            '\n'.join(config_rows),
        )
    return eutran_freqs


def make_eutran_freq_adding_import_file(
    eutran_freq_configs: List[EUtranFrequency],
    date_time: str,
) -> str:
    """Create import file for adding EUtranFrequencies."""
    import_file_path = f'neighbors/reports/G2L_nbr_create_{date_time}.txt'
    eutran_freqs = make_eutran_freq_edff(eutran_freq_configs)
    with open(import_file_path, 'w') as import_file:
        for eutran_freq in eutran_freqs:
            import_file.write(eutran_freq + '\n')
    return import_file_path


def make_eutran_freq_adding_report(
    eutran_freq_configs: List[EUtranFrequency],
    non_existing_cells: List[NeighborPair],
    date_time: str,
) -> str:
    """Create a zip file with EDFF for G2L nbr adding and Excel with nonexistent cells."""
    import_file_path = make_eutran_freq_adding_import_file(eutran_freq_configs, date_time)
    non_existing_cells_file_path = make_nonexistent_cells_report(non_existing_cells, date_time)

    g2l_nbr_adding_zip_path = create_zip_archive(
        import_file_path,
        non_existing_cells_file_path,
        date_time,
    )

    os.remove(import_file_path)
    os.remove(non_existing_cells_file_path)

    return g2l_nbr_adding_zip_path
