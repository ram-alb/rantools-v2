from enmscripting import ElementGroup

from services.enm.enmscripting import EnmScripting


class EnmCli(EnmScripting):
    """A class for communicating with ENM CLI."""

    def get_rnc_rbsid(self, siteid: str) -> ElementGroup:
        """Get RbsId and IubLink data from ENM for a given scope."""
        cmedit_get_command = f'cmedit get * IubLink.(IubLinkId==*{siteid}*, rbsId)'

        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output()
