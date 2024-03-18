from typing import Dict, List, NamedTuple

from neighbors.services.excel import NeighborPair

BAND1_START_EARFCN = 0
BAND3_START_EARFCN = 1200
BAND20_START_EARFCN = 6150

default_params = {
    'qrxlevmin': -124,
    'threshhigh': 6,
}


class EUtranFrequency(NamedTuple):
    """A class representing EUtranFrequency configuration."""

    rnc: str
    cell: str
    eutran_frequency: int
    cellreselectionpriority: int
    threshhigh: int
    qrxlevmin: int
    redirectionorder: int


def prepare_eutran_frequency_configs(
    neighbors: List[NeighborPair],
    controllers: Dict[str, str],
) -> List[EUtranFrequency]:
    """Prepare data for EUtranFrequency MO configuration."""
    eutran_freq_configs = []
    for nbr_pair in neighbors:
        cell = nbr_pair.source

        eutran_earfcn = int(nbr_pair.target)
        if eutran_earfcn >= BAND20_START_EARFCN:
            cellreselectionpriority = 5
            redirectionorder = 3
        elif eutran_earfcn >= BAND3_START_EARFCN:
            cellreselectionpriority = 6
            redirectionorder = 2
        elif eutran_earfcn >= BAND1_START_EARFCN:
            cellreselectionpriority = 7
            redirectionorder = 1

        eutran_freq_configs.append(EUtranFrequency(
            rnc=controllers[cell],
            cell=cell,
            eutran_frequency=eutran_earfcn,
            threshhigh=default_params['threshhigh'],
            qrxlevmin=default_params['qrxlevmin'],
            redirectionorder=redirectionorder,
            cellreselectionpriority=cellreselectionpriority,
        ))
    return eutran_freq_configs
