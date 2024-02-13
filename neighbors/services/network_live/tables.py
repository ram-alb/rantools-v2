from typing import Set

from services.db.connector import DBConnector
from services.db.network_live import BaseTable, Tables


class GsmTable(BaseTable):
    """A class for accessing and interacting with a network live's table of GSM cells."""

    def get_enm_cells(self) -> Set[str]:
        """Get the GSM cells configured on ENM from network live table."""
        table_name = self._get_table_name()
        sql_select = f"SELECT cell FROM {table_name} WHERE oss LIKE 'ENM%'"

        with self.connection.cursor() as cursor:
            cursor.execute(sql_select)
            gsm_cells = cursor.fetchall()

        self._close_connection()

        return {cell[0] for cell in gsm_cells}

    def _get_table_name(self) -> str:
        """Get the table name with the GSM cells."""
        return Tables.gsm_cells.value


class WcdmaTable(BaseTable):
    """A class for accessing and interacting with a network live's table of WCDMA cells."""

    def get_enm_cells(self) -> Set[str]:
        """Get the WCDMA cells configured on ENM from network live table."""
        table_name = self._get_table_name()
        sql_select = f"SELECT utrancell FROM {table_name} WHERE oss LIKE 'ENM%'"

        with self.connection.cursor() as cursor:
            cursor.execute(sql_select)
            wcdma_cells = cursor.fetchall()

        self._close_connection()

        return {cell[0] for cell in wcdma_cells}

    def _get_table_name(self) -> str:
        """Get the table name with the WCDMA cells."""
        return Tables.wcdma_cells.value


def get_network_cells(technology: str) -> Set[str]:
    """Get the cells from the network live based on the technology."""
    tables = {
        'GSM': GsmTable,
        'WCDMA': WcdmaTable,
    }

    table = tables[technology](DBConnector.get_connection())
    return table.get_enm_cells()
