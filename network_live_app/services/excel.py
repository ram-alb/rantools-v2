"""Create excel file with network live cell data."""
from io import BytesIO

import pandas as pd

from network_live_app.services.select import NetworkLiveData


def create_excel(network_live_data: NetworkLiveData) -> bytes:
    """Create excel file with network live cell data."""
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for technology, (rows, headers) in network_live_data.items():
            if not rows:
                continue  # Пропускаем, если данных нет

            df = pd.DataFrame(rows, columns=headers)
            df.to_excel(writer, sheet_name=technology.upper(), index=False)

    output.seek(0)
    return output.getvalue()
