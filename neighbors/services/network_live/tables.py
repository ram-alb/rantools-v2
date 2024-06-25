from typing import List, NamedTuple

from services.db.network_live import BaseTable, Tables


class Cell(NamedTuple):
    """A class representing cell object from Network Live."""

    controller: str
    cell: str


class GsmTable(BaseTable):
    """A class for accessing and interacting with a network live's table of GSM cells."""

    def get_enm_cells(self, enm: str) -> List[Cell]:
        """Get the GSM cells configured on ENM from network live table."""
        table_name = self._get_table_name()
        sql_select = f"SELECT bscname, cell FROM {table_name} WHERE oss = :oss"

        with self.connection.cursor() as cursor:
            cursor.execute(sql_select, oss=enm)
            cursor.rowfactory = Cell
            gsm_cells = cursor.fetchall()

        self._close_connection()

        return gsm_cells

    def _get_table_name(self) -> str:
        """Get the table name with the GSM cells."""
        return Tables.gsm_cells.value


class WcdmaTable(BaseTable):
    """A class for accessing and interacting with a network live's table of WCDMA cells."""

    def get_enm_cells(self, enm: str) -> List[Cell]:
        """Get the WCDMA cells configured on ENM from network live table."""
        table_name = self._get_table_name()
        sql_select = f"SELECT rncname, utrancell FROM {table_name} WHERE oss = :oss"

        with self.connection.cursor() as cursor:
            cursor.execute(sql_select, oss=enm)
            cursor.rowfactory = Cell
            wcdma_cells = cursor.fetchall()

        self._close_connection()

        return wcdma_cells

    def _get_table_name(self) -> str:
        """Get the table name with the WCDMA cells."""
        return Tables.wcdma_cells.value
