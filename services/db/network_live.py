import enum
from abc import abstractmethod
from typing import List, NamedTuple


class Cell(NamedTuple):
    """A class representing cell object from Network Live."""

    controller: str
    cell: str


class Tables(enum.Enum):
    """Enumeration representing a set of Network Live table names."""

    gsm_cells = 'gsmcells2'
    wcdma_cells = 'wcdmacells2'
    lte_cells = 'ltecells2'
    nr_cells = 'nrcells'


class BaseTable:
    """A class presenting basic methods to work with Network Live tables."""

    def __init__(self, connection):
        """Initiate table instance."""
        self.connection = connection

    @abstractmethod
    def get_enm_cells(self, enm: str) -> List[Cell]:
        """Abstract method for retrieving the cell names configured on ENM from Network Live db."""
        pass

    @abstractmethod
    def _get_table_name(self) -> str:
        """Abstract method for retrieving the table name."""
        pass

    def _close_connection(self) -> None:
        """Close connection to Network Live db."""
        self.connection.close()
