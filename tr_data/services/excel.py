from io import BytesIO
from typing import List

import pandas as pd  # type: ignore


def create_tr_excel(columns_list: List[str], tr_data: List[tuple]) -> bytes:
    """Create an Excel file with the TR data."""
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df = pd.DataFrame(tr_data, columns=columns_list)
        df.to_excel(writer, sheet_name='SITE_TR_DATA', index=False)

    output.seek(0)
    return output.getvalue()
