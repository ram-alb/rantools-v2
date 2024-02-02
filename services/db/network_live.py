import enum
from abc import abstractmethod
from typing import Type


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
    def _get_table_name(self) -> Type[Tables]:
        """Abstract method for retrieving the table name."""
        pass

    def _close_connection(self):
        """Close connection to Network Live db."""
        self.connection.close()
