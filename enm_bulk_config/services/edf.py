from typing import Dict, List, Tuple

from enm_bulk_config.services.edff.eutrancellfdd import generate_lte_rach_config_lines
from enm_bulk_config.services.parameters import EutranCellFddParams, NRCellDUParams
from services.technologies import Technologies


def _get_lte_pci_config_lines(pci) -> Tuple[str, str]:
    """
    Return config lines for PCI.

    Return physicalLayerCellIdGroup and physicalLayerSubCellId based on PCI value.
    Handles string, int, empty, or invalid input gracefully.
    """
    try:
        pci_float = float(pci)
        pci_int = int(pci_float)
        cell_id_group = pci_int // 3
        sub_cell_id = pci_int % 3
        return (
            f"physicalLayerCellIdGroup:{cell_id_group}",
            f"physicalLayerSubCellId:{sub_cell_id}",
        )
    except (TypeError, ValueError):
        return ("physicalLayerCellIdGroup:", "physicalLayerSubCellId:")


def _generate_lte_pci_config_lines(fdns: List[dict]) -> List[str]:
    lines = []
    for fdn_data in fdns:
        fdn = fdn_data.get("fdn")
        pci = fdn_data.get(EutranCellFddParams.pci.value)
        if not fdn or pci is None:
            continue
        cell_id_group, sub_cell_id = _get_lte_pci_config_lines(pci)
        lines.append("SET")
        lines.append(f'FDN:"{fdn}"')
        lines.append(cell_id_group)
        lines.append(sub_cell_id)
        lines.append("")
    return lines


def _generate_nr_pci_config_lines(fdns: List[dict]) -> List[str]:
    lines = []
    for fdn_data in fdns:
        fdn = fdn_data.get("fdn")
        pci = fdn_data.get(NRCellDUParams.pci.value)
        if not fdn or pci is None:
            continue
        lines.append("SET")
        lines.append(f'FDN:"{fdn}"')
        lines.append("administrativeState:LOCKED")
        lines.append(f"nRPCI:{pci}")
        lines.append("")

        lines.append("SET")
        lines.append(f'FDN:"{fdn}"')
        lines.append("administrativeState:UNLOCKED")
        lines.append("")

    return lines


def generate_edf_config(
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
        ): _generate_lte_pci_config_lines,
        (
            Technologies.nr.value,
            NRCellDUParams.pci.value,
        ): _generate_nr_pci_config_lines,
        (
            Technologies.lte.value,
            EutranCellFddParams.rach.value,
        ): generate_lte_rach_config_lines,
    }

    config = {}

    for enm, fdns in fdn_params.items():
        config_generator = config_generators.get((technology, parameter))
        config[enm] = "\n".join(config_generator(fdns))
    return config
