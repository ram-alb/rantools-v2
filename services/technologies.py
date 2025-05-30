from enum import Enum


class Technologies(Enum):
    """Enumeration representing a set of technologies."""

    lte = "LTE"

    @classmethod
    def get_technologies(cls):
        """Return a list of all technologies."""
        return [tech.value for tech in cls]

    @classmethod
    def from_str(cls, tech_name: str) -> "Technologies":
        """
        Get Technologies enum member by string (case-insensitive).

        Raises ValueError if not found.
        """
        for tech in cls:
            if tech.value.lower() == tech_name.lower():
                return tech
        raise ValueError(f"Unknown technology: {tech_name}")
