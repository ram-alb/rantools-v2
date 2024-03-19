from enmscripting import ElementGroup  # type: ignore

from services.enm.enmscripting import EnmScripting


class EnmCli(EnmScripting):
    """A class for communicating with ENM CLI."""

    def get_bsc_tg(self, scope: str, tg_type: str) -> ElementGroup:
        """Get TG data from ENM for a given scope."""
        tg_types = {
            'G12': 'G12Tg',
            'G31': 'G31Tg',
        }

        tg = tg_types[tg_type]
        cmedit_get_command = f'cmedit get {scope} {tg}.{tg}Id'

        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output()
