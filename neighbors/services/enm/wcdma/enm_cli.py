from typing import Set, Tuple

from enmscripting import ElementGroup  # type: ignore

from services.enm.enmscripting import EnmScripting


class EnmCli(EnmScripting):
    """The service for obtaining ENM data."""

    def __init__(self, enm_server: str, rnc_set: Set[str], bsc_set: Set[str]):
        """Initialize attributes for an EnmCli instance."""
        super().__init__(enm_server)
        self.rnc_set = rnc_set
        self.bsc_set = bsc_set

    def get_gerancell_params(self) -> Tuple[ElementGroup, str]:
        """Get the ENM data with the necessary gerancell level parameters."""
        params_list = [
            'bcc',
            'bcchNo',
            'cgi',
            'ncc',
        ]
        cmedit_get_command = 'cmedit get {scope} GeranCell.({params})'.format(
            scope=self._get_bsc_scope(),
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output(), self._get_last_parameter(params_list)

    def get_utran_cells(self) -> ElementGroup:
        """Get the ENM data with utrancell FDNs."""
        cmedit_get_command = 'cmedit get {scope} UtranCell'.format(
            scope=self._get_rnc_scope(),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output()

    def get_external_gsm_network_data(self) -> ElementGroup:
        """Get the ENM data with external gsm network id."""
        cmedit_get_command = 'cmedit get {scope} ExternalGsmNetwork.(mnc==2)'.format(
            scope=self._get_rnc_scope(),
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
