from io import BytesIO
from typing import Dict, List

import pandas as pd  # type: ignore


def save_retsubunits_to_excel(retsubunits: List[Dict[str, str]]):
    """Save RetSubUnit data to an Excel file."""
    column_order = [
        "ENM",
        "NodeId",
        "Sector",
        "AntennaNearUnitId",
        "electricalAntennaTilt",
        "iuantAntennaModelNumber",
        "maxTilt",
        "minTilt",
    ]

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df = pd.DataFrame(retsubunits)
        df = df[column_order].fillna("")
        df.to_excel(writer, sheet_name="RetSubUnit", index=False)

    output.seek(0)
    return output
