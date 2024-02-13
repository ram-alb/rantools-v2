import os

import enmscripting


class EnmScripting:
    """A class providing comunication with the ENM via enmscripting."""

    def __init__(self, enm_server):
        """Initialize attributes for an EnmScripting instance."""
        self.enm_server = enm_server

    def _get_session(self):
        """Get enmscripting session for comunication with ENM."""
        return enmscripting.open(self.enm_server).with_credentials(
            enmscripting.UsernameAndPassword(
                os.getenv('ENM_LOGIN'),
                os.getenv('ENM_PASSWORD'),
            ),
        )

    def _close_session(self, session):
        """Close enmscripting session."""
        enmscripting.close(session)

    def _get_last_parameter(self, params_list):
        """Get the name of the last parameter from the provided parameter list."""
        return sorted(params_list)[-1]
