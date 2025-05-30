import io
import zipfile
from typing import Dict

import pandas as pd


def create_archive(edf_config: Dict[str, str], non_existent_df: pd.DataFrame) -> bytes:
    """Create a ZIP archive containing EDF config scripts and non-existent cells Excel file."""
    archive_buffer = io.BytesIO()
    with zipfile.ZipFile(archive_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for enm, text in edf_config.items():
            filename = f"{enm}_config.txt"
            zf.writestr(filename, text)

        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            non_existent_df.to_excel(writer, index=False)
        excel_buffer.seek(0)
        zf.writestr("non_existent_cells.xlsx", excel_buffer.read())

    archive_buffer.seek(0)
    return archive_buffer.getvalue()
