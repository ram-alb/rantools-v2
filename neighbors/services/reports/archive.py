import os
import zipfile


def create_zip_archive(file1_path: str, file2_path: str, date_time: str) -> str:
    """Create a zip archive with two files."""
    output_zip_path = f'neighbors/reports/nbr_{date_time}.zip'
    with zipfile.ZipFile(output_zip_path, 'w') as zipf:
        zipf.write(file1_path, os.path.basename(file1_path))
        zipf.write(file2_path, os.path.basename(file2_path))

    return output_zip_path
