from typing import Dict

from enmscripting import ElementGroup  # type: ignore

from services.enm.enmscripting import EnmScripting


class EnmCli(EnmScripting):
    """A class for communicating with ENM CLI."""

    def get_controllers(self) -> Dict[str, ElementGroup]:
        """Retrieve configured BSCs and RNCs from ENM."""
        commands = {
            'bsc': "cmedit get * MeContext.(neType=='BSC') -t",
            'rnc': "cmedit get * MeContext.(neType=='RNC') -t",
        }

        session = self._get_session()
        cmd = session.command()

        controllers = {
            controller: cmd.execute(command).get_output()
            for controller, command in commands.items()
        }

        self._close_session(session)

        return controllers
