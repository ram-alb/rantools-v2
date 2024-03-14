from typing import Dict, List, NamedTuple

from neighbors.services.excel import NeighborPair

BAND1_START_EARFCN = 0
BAND3_START_EARFCN = 1200
BAND20_START_EARFCN = 6150

default_params = {
    'hPrioThrE': 3,
    'lPrioThrE': 3,
    'qRxLevMinE': 3,
}


class EUtranFrequency(NamedTuple):
    """A class representing EUtranFrequency configuration."""

    bsc: str
    cell: str
    eutran_frequency: int
    h_prio_thr_e: int
    l_prio_thr_e: int
    q_rxlev_min_e: int
    rat_prio_e: int


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
            rat_prio_e = 5
        elif eutran_earfcn >= BAND3_START_EARFCN:
            rat_prio_e = 6
        elif eutran_earfcn >= BAND1_START_EARFCN:
            rat_prio_e = 7

        eutran_freq_configs.append(EUtranFrequency(
            bsc=controllers[cell],
            cell=cell,
            eutran_frequency=eutran_earfcn,
            h_prio_thr_e=default_params['hPrioThrE'],
            l_prio_thr_e=default_params['lPrioThrE'],
            q_rxlev_min_e=default_params['qRxLevMinE'],
            rat_prio_e=rat_prio_e,
        ))
    return eutran_freq_configs
