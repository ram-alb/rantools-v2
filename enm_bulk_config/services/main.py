import io
from typing import Tuple

import pandas as pd

from enm_bulk_config.services.edff.main import generate_edff_config
from enm_bulk_config.services.enm import get_fdn_params
from enm_bulk_config.services.files import create_archive
from enm_bulk_config.services.network_live import get_network_live_df
from enm_bulk_config.services.templates import read_clean_excel


def _split_cells_by_existence(
    template_df: pd.DataFrame,
    nl_df: pd.DataFrame,
    parameter: str,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split cells into two DataFrames.

    1. Cells from nl_df that exist in template_df['cell'].
    2. Cells from template_df that do not exist in nl_df['cell'].
    """
    cell_col = "cell"
    template_cells = template_df[cell_col].astype(str)
    nl_cells = nl_df[cell_col].astype(str)

    # 1. Cells from nl_df that exist in template_df
    existent_df = nl_df[nl_df[cell_col].astype(str).isin(template_cells)].copy()
    # Merge parameter column from template_df
    existent_df = existent_df.merge(
        template_df[[cell_col, parameter]].astype({cell_col: str}),
        on=cell_col,
        how="left",
    )
    existent_df = existent_df[existent_df[parameter].notnull()]
    existent_df = existent_df[existent_df[parameter].astype(str).str.strip() != ""]
    existent_df[parameter] = existent_df[parameter].astype(str).str.strip()

    # 2. Cells from template_df that do not exist in nl_df
    non_existent_df = template_df[
        ~template_df[cell_col].astype(str).isin(nl_cells)
    ].copy()

    return existent_df, non_existent_df


def main(technology: str, parameter: str, template: io.BytesIO) -> bytes:
    """Generate EDF config script and non-existent cells Excel."""
    # get the template content
    template_df = read_clean_excel(template)

    # select data from db
    nl_df = get_network_live_df(technology)

    # filter template data by db data to existent and non-existent cells
    existent_df, non_existent_df = _split_cells_by_existence(
        template_df,
        nl_df,
        parameter,
    )

    # get fdns from ENMs
    fdn_params = get_fdn_params(technology, existent_df, parameter)

    # with existent cells create enm bulk config script
    config = generate_edff_config(fdn_params, technology, parameter)
    # return script and non-existent cells
    return create_archive(config, non_existent_df)
