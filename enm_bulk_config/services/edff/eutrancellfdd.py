from typing import List

from enm_bulk_config.services.parameters import EutranCellFddParams


def generate_lte_rach_config_lines(fdns: List[dict]) -> List[str]:
    """Generate EDF config lines for LTE RACH."""
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
