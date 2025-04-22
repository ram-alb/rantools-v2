from io import BytesIO
from typing import List

import pandas as pd  # type: ignore


def write_diffs_to_excel(diffs: List[dict]) -> bytes:
    """Write differences to an Excel file."""
    df = pd.DataFrame(diffs)
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']

        for ind, column in enumerate(df.columns):
            max_length = max(
                df[column].astype(str).map(len).max(),
                len(column),
            )
            adjusted_width = max_length + 2
            worksheet.set_column(ind, ind, adjusted_width)

    output.seek(0)
    return output.getvalue()
