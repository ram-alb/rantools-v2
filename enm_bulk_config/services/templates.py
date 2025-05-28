from io import BytesIO

from openpyxl import Workbook


def generate_bulk_template(technology: str, parameter: str) -> bytes:
    """Generate an Excel template for bulk configuration."""
    wb = Workbook()
    ws = wb.active
    ws.title = f"{technology}_{parameter}"
    ws.append(["cell", f"new {parameter}"])
    output = BytesIO()
    wb.save(output)
    return output.getvalue()
