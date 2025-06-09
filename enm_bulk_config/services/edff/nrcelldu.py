from typing import List

from enm_bulk_config.services.parameters import NRCellDUParams


def _generate_unlock_fdn_lines(fdn: str) -> List[str]:
    """Generate EDFF config lines for unlocking an FDN."""
    lines = []
    lines.append("SET")
    lines.append(f'FDN:"{fdn}"')
    lines.append("administrativeState:UNLOCKED")
    lines.append("")
    return lines


def generate_nr_pci_config_lines(fdns: List[dict]) -> List[str]:
    """Generate EDFF config lines for NR PCI."""
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

        lines.extend(_generate_unlock_fdn_lines(fdn))

    return lines
