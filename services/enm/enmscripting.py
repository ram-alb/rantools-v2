import os
from enum import Enum
from typing import List

import enmscripting  # type: ignore
from enmscripting.enmsession import EnmSession  # type: ignore


class Enms(Enum):
    """Enum for ENM servers."""

    ENM2 = "ENM_2"
    ENM4 = "ENM_4"


class EnmScripting:
    """A class providing comunication with the ENM via enmscripting."""

    def __init__(self, enm_server: str):
        """Initialize attributes for an EnmScripting instance."""
        self.enm_server = self._get_server(enm_server)

    def _get_server(self, enm_pointer):
        """Retrieve the ENM server address from environment variables."""
        enm_server = os.getenv(enm_pointer)
        if enm_server is None:
            raise ValueError(f'No {enm_pointer} environment variable')
        return enm_server

    def _get_session(self) -> EnmSession:
        """Get enmscripting session for comunication with ENM."""
        return enmscripting.open(self.enm_server).with_credentials(
            enmscripting.UsernameAndPassword(
                os.getenv('ENM_LOGIN'),
                os.getenv('ENM_PASSWORD'),
            ),
        )

    def _close_session(self, session: EnmSession) -> None:
        """Close enmscripting session."""
        enmscripting.close(session)

    def _get_last_parameter(self, params_list: List[str]) -> str:
        """Get the name of the last parameter from the provided parameter list."""
        return sorted(params_list)[-1]
