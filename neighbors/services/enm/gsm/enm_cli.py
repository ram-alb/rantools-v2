from typing import Tuple

from enmscripting import ElementGroup  # type: ignore

from services.enm.enmscripting import EnmScripting


class EnmCLI(EnmScripting):
    """The service for obtaining ENM data."""

    def get_rnc_function_params(self) -> Tuple[ElementGroup, str]:
        """Get the ENM data with the necessary RNC level parameters."""
        params_list = [
            'mcc',
            'mnc',
            'rncId',
        ]
        cmedit_get_command = 'cmedit get * RncFunction.({params})'.format(
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
        cmedit_get_command = 'cmedit get * UtranCell.({params})'.format(
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output(), self._get_last_parameter(params_list)

    def get_geran_cells(self) -> ElementGroup:
        """Get Geran cells' FDNs."""
        cmedit_get_command = 'cmedit get * GeranCell'
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output()
