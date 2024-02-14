from typing import Any, Tuple

from services.enm.enmscripting import EnmScripting


class EnmCli(EnmScripting):
    def get_gerancell_params(self) -> Tuple[Any, Any]:
        params_list = [
            'bcc',
            'bcchNo',
            'cgi',
            'ncc',
        ]
        cmedit_get_command = 'cmedit get * GeranCell.({params})'.format(
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output(), self._get_last_parameter(params_list)

    def get_utran_cells(self):
        cmedit_get_command = 'cmedit get * UtranCell'
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output()

    def get_external_gsm_network_data(self):
        cmedit_get_command = 'cmedit get * ExternalGsmNetwork.(mnc==2)'
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return response.get_output()
