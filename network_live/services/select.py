"""Select cell data from network_live."""

from services.db.network_live import Tables
from services.db.connector import DBConnector


def select_data(technologies):
    """
    Select cell data from network_live.

    Args:
        technologies: list 

    Returns:
        dict: A dictionary containing data for each technology.
    """
    network_live_tables = {
        'lte': Tables.lte_cells.value,
        'wcdma': Tables.wcdma_cells.value,
        'gsm': Tables.gsm_cells.value,
        'nr': Tables.nr_cells.value,
    }
    network_live_data = {}

    with DBConnector.get_connection() as connection:
        cursor = connection.cursor()
        for technology in technologies:
            sql_select = 'SELECT * FROM {table}'.format(table=network_live_tables[technology])
            network_live_data[technology] = cursor.execute(sql_select).fetchall()

    return network_live_data