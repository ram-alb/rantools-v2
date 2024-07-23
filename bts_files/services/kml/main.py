from bts_files.services.filter_cells import AllTechPolygon
from bts_files.services.kml.placemark import make_kml_folder
from bts_files.services.kml.template import render_template


def make_kml_content(bts_data: AllTechPolygon) -> str:
    """Generate KML content with folders for each technology's placemarks."""
    kml_content = render_template('template.kml')

    for technology, placemark_data in bts_data.items():
        folder = make_kml_folder(placemark_data, technology)  # type: ignore
        kml_content += folder

    kml_content += '\n</Document>\n</kml>'

    return kml_content
