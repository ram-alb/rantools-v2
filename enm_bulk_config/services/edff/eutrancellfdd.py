from typing import List, Tuple

from enm_bulk_config.services.parameters import EutranCellFddParams


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


def generate_lte_pci_config_lines(fdns: List[dict]) -> List[str]:
    """Generate EDFF config lines for LTE PCI."""
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


def generate_lte_rach_config_lines(fdns: List[dict]) -> List[str]:
    """Generate EDFF config lines for LTE RACH."""
    lines = []

    for fdn_data in fdns:
        fdn = fdn_data.get("fdn")
        rach = fdn_data.get(EutranCellFddParams.rach.value)
        if not fdn or rach is None:
            continue
        lines.append("SET")
        lines.append(f'FDN:"{fdn}"')
        lines.append(f"rachRootSequence:{rach}")
        lines.append("")

    return lines
