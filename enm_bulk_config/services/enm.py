import re
from typing import Dict, List, Optional, Set, Tuple

import pandas as pd
from enm_cli import cmedit_get
from enmscripting import ElementGroup

from services.technologies import Technologies

Cells = Set[str]
Scope = List[Tuple[str, str, Cells]]


def _get_enm_scope(existent_df: pd.DataFrame) -> Scope:
    """Group sitenames and cells by 'oss' value."""
    scope = []
    for oss, group in existent_df.groupby("enm"):
        sitenames = group["sitename"].dropna().astype(str).unique()
        sitenames_str = ";".join(sitenames)
        cells = set(group["cell"].dropna().astype(str).unique())
        scope.append((oss, sitenames_str, cells))
    return scope


def _extract_mo_value(fdn: str, technology: str) -> Optional[str]:
    patterns = {
        Technologies.lte: "EUtranCellFDD=([^, ]+)",
    }
    pattern = patterns.get(Technologies.from_str(technology))
    match = re.search(pattern, fdn) if pattern else None
    return match.group(1) if match else None


def _get_enm_data(
    technology: str,
    scope: Scope,
) -> Dict[str, Tuple[ElementGroup, set]]:
    mo_types = {
        Technologies.lte: "EUtranCellFDD",
    }
    tech_enum = Technologies.from_str(technology)
    mo_type = mo_types.get(tech_enum)
    if not mo_type:
        raise ValueError(f"MO type not defined for technology: {technology}")

    raw_results = {}
    for enm_name, node_names, cell_names in scope:
        command = f"cmedit get {node_names} {mo_type}"
        raw_results[enm_name] = (cmedit_get(enm_name, command), cell_names)
    return raw_results


def get_fdn_params(
    technology: str,
    existent_df: pd.DataFrame,
    parameter: str,
) -> Dict[str, List[dict]]:
    """Return a dict with {fdn: <fdn_val>, param_name: param_val}.

    For each FDN found in ENM output,
    where param_val is taken from existent_df for the corresponding cell.
    """
    scope = _get_enm_scope(existent_df)
    enm_data = _get_enm_data(technology, scope)

    param_map = dict(zip(existent_df["cell"].astype(str), existent_df[parameter]))

    fdn_params = {}
    for enm, (output_lines, cells) in enm_data.items():
        for line in output_lines:
            line_value = line.value()
            if "FDN" in line_value:
                cell_name = _extract_mo_value(line_value, technology)
                if cell_name and cell_name in cells:
                    param_val = param_map.get(cell_name)
                    fdn_params.setdefault(enm, []).append(
                        {
                            "fdn": line_value.split(" : ")[-1],
                            parameter: param_val,
                        },
                    )
    return fdn_params
