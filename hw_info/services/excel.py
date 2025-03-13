from io import BytesIO
from typing import List

import pandas as pd  # type: ignore


def create_hw_excel(columns_list: List[str], hw_data: List[tuple]) -> bytes:
    """Create an Excel file with the HW info."""
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df = pd.DataFrame(hw_data, columns=columns_list)
        df.to_excel(writer, sheet_name='HW_INFO', index=False)

    output.seek(0)
    return output.getvalue()
