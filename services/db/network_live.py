import enum
from abc import abstractmethod


class Tables(enum.Enum):
    """Enumeration representing a set of Network Live table names."""

    gsm_cells = "gsmcells2"
    wcdma_cells = "wcdmacells2"
    lte_cells = "ltecells2"
    nr_cells = "nrcells"
    iot_cells = "iotcells"

    @classmethod
    def get_table(cls, technology: str) -> "Tables":
        """Get table enum by technology name (case-insensitive)."""
        tech_map = {
            "GSM": cls.gsm_cells,
            "WCDMA": cls.wcdma_cells,
            "LTE": cls.lte_cells,
            "NR": cls.nr_cells,
            "IOT": cls.iot_cells,
        }
        try:
            return tech_map[technology.upper()]
        except KeyError:
            raise ValueError(f"Unknown technology: {technology}")


class BaseTable:
    """A class presenting basic methods to work with Network Live tables."""

    def __init__(self, connection):
        """Initiate table instance."""
        self.connection = connection

    @abstractmethod
    def _get_table_name(self) -> str:
        """Abstract method for retrieving the table name."""
        pass

    def _close_connection(self) -> None:
        """Close connection to Network Live db."""
        self.connection.close()
