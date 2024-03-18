import os
from typing import List

from neighbors.services.excel import NeighborPair
from neighbors.services.reports.archive import create_zip_archive
from neighbors.services.reports.nonexistent_cells import make_nonexistent_cells_report
from neighbors.services.wcdma.u2l.config_preparator import EUtranFrequency


def make_eutran_freq_edff(eutran_freq_configs: List[EUtranFrequency]) -> List[str]:
    """Create an EDFF part for configuring EUtranFrequency."""
    eutran_freqs = []
    for config in eutran_freq_configs:
        config_rows = ['create']
        fdn = (
            f'FDN : "SubNetwork=RNC,MeContext={config.rnc},ManagedElement=1,'
            f'RncFunction=1,UtranCell={config.cell},EutranFreqRelation={config.eutran_frequency}"'
        )
        config_rows.append(fdn)
        config_rows.append(
            f'eutranFrequencyRef : "SubNetwork=RNC,MeContext={config.rnc},ManagedElement=1,'
            f'RncFunction=1,EutraNetwork=1,EutranFrequency={config.eutran_frequency}"',
        )
        config_rows.append(f'cellReselectionPriority : {config.cellreselectionpriority}')
        config_rows.append(f'threshHigh : {config.threshhigh}')
        config_rows.append(f'qRxLevMin : {config.qrxlevmin}')
        config_rows.append(f'redirectionOrder : {config.redirectionorder}')
        eutran_freqs.append(
            '\n'.join(config_rows),
        )
    return eutran_freqs


def make_eutran_freq_adding_import_file(
    eutran_freq_configs: List[EUtranFrequency],
    date_time: str,
) -> str:
    """Create EDFF import file for UMTS adding EUtranFrequencies."""
    import_file_path = f'neighbors/reports/U2L_nbr_create_{date_time}.txt'
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
    """Create a zip file with EDFF for U2L freq adding and Excel with nonexistent cells."""
    import_file_path = make_eutran_freq_adding_import_file(eutran_freq_configs, date_time)
    non_existing_cells_file_path = make_nonexistent_cells_report(non_existing_cells, date_time)

    u2l_nbr_adding_zip_path = create_zip_archive(
        import_file_path,
        non_existing_cells_file_path,
        date_time,
    )

    os.remove(import_file_path)
    os.remove(non_existing_cells_file_path)

    return u2l_nbr_adding_zip_path
