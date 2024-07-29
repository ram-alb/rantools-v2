from typing import List

from bts_files.services.atoll.main import select_atoll_data
from bts_files.services.excel import make_excel_content
from bts_files.services.filter_cells import filter_cells
from bts_files.services.kml.main import make_kml_content
from bts_files.services.nemo_nbf import make_nbf_content


def get_file_content(file_type: str, technologies: List[str], regions: List[str]):
    """Generate content for the specified file type based on the technologies and regions."""
    content_funcs = {
        'kml': make_kml_content,
        'nbf': make_nbf_content,
        'excel': make_excel_content,
    }
    selected_atoll_cells = select_atoll_data(technologies)
    filtered_data = filter_cells(selected_atoll_cells, regions)

    return content_funcs[file_type](filtered_data)
