from typing import Set, Tuple

from enmscripting import ElementGroup  # type: ignore

from services.enm.enmscripting import EnmScripting


class EnmCli(EnmScripting):
    """The service for obtaining ENM data."""

    def __init__(self, enm_server: str, rnc_set: Set[str]):
        """Initialize attributes for an EnmCli instance."""
        super().__init__(enm_server)
        self.rnc_set = rnc_set

    def get_utran_cell_params(self) -> Tuple[ElementGroup, str]:
        """Get the ENM data with the necessary UtranCell parameters."""
        params_list = [
            'cId',
            'locationAreaRef',
            'maxTxPowerUl',
            'primaryCpichPower',
            'primaryScramblingCode',
            'routingAreaRef',
            'reportingRange1a',
            'reportingRange1b',
            'uarfcnDl',
            'uarfcnUl',
        ]

        cmedit_get_command = 'cmedit get {scope} UtranCell.({params})'.format(
            scope=self._get_scope(),
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output(), self._get_last_parameter(params_list)

    def _get_scope(self) -> str:
        """Get scope of RNC for cli commands."""
        return ';'.join(self.rnc_set)
