from typing import Dict, List, Tuple


def get_lte_pci_config_lines(pci) -> Tuple[str, str]:
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


def generate_edf_config(
    fdn_params: Dict[str, List[dict]],
    technology: str,
    parameter: str,
) -> Dict[str, str]:
    """
    Generate EDF config text for each ENM.

    Returns dict: enm -> config text.
    """
    config = {}

    for enm, fdns in fdn_params.items():
        lines = []
        for fdn_data in fdns:
            fdn = fdn_data.get("fdn")
            if not fdn:
                continue
            lines.append("SET")
            lines.append(f'FDN:"{fdn}"')

            parameter_value = fdn_data.get(parameter)
            if technology == "LTE" and parameter == "PCI":
                lines.extend(get_lte_pci_config_lines(parameter_value))

            lines.append("")
        config[enm] = "\n".join(lines)
    return config
