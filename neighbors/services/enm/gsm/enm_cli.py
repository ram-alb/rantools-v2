from typing import Set, Tuple

from enmscripting import ElementGroup  # type: ignore

from services.enm.enmscripting import EnmScripting


class EnmCLI(EnmScripting):
    """The service for obtaining ENM data."""

    def __init__(self, enm_server: str, bsc_set: Set[str], rnc_set: Set[str]):
        """Initialize attributes for an EnmCli instance."""
        super().__init__(enm_server)
        self.bsc_set = bsc_set
        self.rnc_set = rnc_set

    def get_rnc_function_params(self) -> Tuple[ElementGroup, str]:
        """Get the ENM data with the necessary RNC level parameters."""
        params_list = [
            'mcc',
            'mnc',
            'rncId',
        ]
        cmedit_get_command = 'cmedit get {scope} RncFunction.({params})'.format(
            scope=self._get_rnc_scope(),
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output(), self._get_last_parameter(params_list)

    def get_utrancell_params(self) -> Tuple[ElementGroup, str]:
        """Get ENM data with the necessary utran cell parameters."""
        params_list = [
            'locationAreaRef',
            'localCellId',
            'primaryScramblingCode',
            'uarfcnDl',
        ]
        cmedit_get_command = 'cmedit get {scope} UtranCell.({params})'.format(
            scope=self._get_rnc_scope(),
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output(), self._get_last_parameter(params_list)

    def get_geran_cells(self) -> ElementGroup:
        """Get Geran cells' FDNs."""
        cmedit_get_command = 'cmedit get {scope} GeranCell'.format(
            scope=self._get_bsc_scope(),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output()

    def _get_bsc_scope(self) -> str:
        """Get scope of BSC for cli commands."""
        return ';'.join(self.bsc_set)

    def _get_rnc_scope(self) -> str:
        """Get scope of RNC for cli commands."""
        return ';'.join(self.rnc_set)
