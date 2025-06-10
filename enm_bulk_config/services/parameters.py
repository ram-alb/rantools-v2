from enum import Enum
from typing import List


class EutranCellFddParams(Enum):
    """Enumeration representing parameters for EutranCellFdd."""

    pci = "PCI"
    rach = "rachRootSequence"

    @classmethod
    def get_params(cls) -> List[str]:
        """Return a list of all parameters for EutranCellFdd."""
        return [parameter.value for parameter in cls]


class NRCellDUParams(Enum):
    """Enumeration representing parameters for NRCellDU."""

    pci = "nRPCI"
    rach = "rachRootSequence"

    @classmethod
    def get_params(cls) -> List[str]:
        """Return a list of all parameters for NRCellDU."""
        return [parameter.value for parameter in cls]


parameters_map = {
    "LTE": EutranCellFddParams.get_params(),
    "NR": NRCellDUParams.get_params(),
}
