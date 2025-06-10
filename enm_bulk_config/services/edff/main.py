from typing import Dict, List

from enm_bulk_config.services.edff.eutrancellfdd import (
    generate_lte_pci_config_lines,
    generate_lte_rach_config_lines,
)
from enm_bulk_config.services.edff.nrcelldu import (
    generate_nr_pci_config_lines,
    generate_nr_rach_config_lines,
)
from enm_bulk_config.services.parameters import EutranCellFddParams, NRCellDUParams
from services.technologies import Technologies


def generate_edff_config(
    fdn_params: Dict[str, List[dict]],
    technology: str,
    parameter: str,
) -> Dict[str, str]:
    """
    Generate EDF config text for each ENM.

    Returns dict: enm -> config text.
    """
    config_generators = {
        (
            Technologies.lte.value,
            EutranCellFddParams.pci.value,
        ): generate_lte_pci_config_lines,
        (
            Technologies.nr.value,
            NRCellDUParams.pci.value,
        ): generate_nr_pci_config_lines,
        (
            Technologies.lte.value,
            EutranCellFddParams.rach.value,
        ): generate_lte_rach_config_lines,
        (
            Technologies.nr.value,
            NRCellDUParams.rach.value,
        ): generate_nr_rach_config_lines,
    }

    config = {}

    for enm, fdns in fdn_params.items():
        config_generator = config_generators.get((technology, parameter))
        config[enm] = "\n".join(config_generator(fdns))
    return config
