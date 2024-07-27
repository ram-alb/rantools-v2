from enmscripting import ElementGroup  # type: ignore

from services.enm.enmscripting import EnmScripting


class EnmCli(EnmScripting):
    """A class used to interact with ENM CLI for specific tasks."""

    def get_lte_tx_data(self, site_id: str) -> ElementGroup:
        """Fetch LTE tx nums data for a specified site ID."""
        command = f'cmedit get *{site_id}* SectorCarrier.(noOfTxAntennas, reservedBy) -t'

        session = self._get_session()
        cmd = session.command()
        response = cmd.execute(command)
        self._close_session(session)

        return response.get_output()
