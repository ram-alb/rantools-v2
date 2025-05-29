from enum import Enum


class Technologies(Enum):
    """Enumeration representing a set of technologies."""

    gsm = "GSM"
    wcdma = "WCDMA"
    lte = "LTE"
    nr = "NR"
    iot = "IoT"

    @classmethod
    def get_technologies(cls):
        """Return a list of all technologies."""
        return [tech.value for tech in cls]
