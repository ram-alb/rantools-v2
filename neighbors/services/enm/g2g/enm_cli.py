from typing import NamedTuple, Set

from enmscripting import ElementGroup  # type: ignore

from services.enm.enmscripting import EnmScripting


class EnmData(NamedTuple):
    """A class representing data returned by EnmCli."""

    cmd_output: ElementGroup
    last_parameter: str


class EnmCli(EnmScripting):
    """The service for obtaining ENM data."""

    def __init__(self, enm_server: str, bsc_set: Set[str]):
        """Initialize attributes for an EnmCli instance."""
        super().__init__(enm_server)
        self.bsc_set = bsc_set

    def get_power_control_dl_params(self) -> EnmData:
        """Get the ENM data with the necessary PowerControlDownlink parameters."""
        params_list = [
            'bsPwr',
            'bsTxPwr',
        ]
        cmedit_get_command = 'cmedit get {scope} PowerControlDownlink.({params})'.format(
            scope=self._get_scope(),
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return EnmData(
            cmd_output=response.get_output(),
            last_parameter=self._get_last_parameter(params_list),
        )

    def get_power_control_ul_params(self) -> EnmData:
        """Get the ENM data with the necessary PowerControlUplink parameters."""
        params_list = [
            'bsRxMin',
            'bsRxSuff',
            'msRxSuff',
            'msTxPwr',
        ]
        cmedit_get_command = 'cmedit get {scope} PowerControlUplink.({params})'.format(
            scope=self._get_scope(),
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return EnmData(
            cmd_output=response.get_output(),
            last_parameter=self._get_last_parameter(params_list),
        )

    def get_hierarchical_cell_structure_params(self) -> EnmData:
        """Get the ENM data with the necessary HierarchicalCellStructure parameters."""
        params_list = [
            'fastMsReg',
            'layer',
            'layerHyst',
            'layerThr',
            'pSsTemp',
            'pTimTemp',
        ]
        cmedit_get_command = 'cmedit get {scope} HierarchicalCellStructure.({params})'.format(
            scope=self._get_scope(),
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return EnmData(
            cmd_output=response.get_output(),
            last_parameter=self._get_last_parameter(params_list),
        )

    def get_geran_cell_params(self) -> EnmData:
        """Get the ENM data with the necessary GeranCell parameters."""
        params_list = [
            'bcc',
            'bcchNo',
            'cSysType',
            'cgi',
            'ncc',
        ]
        cmedit_get_command = 'cmedit get {scope} GeranCell.({params})'.format(
            scope=self._get_scope(),
            params=','.join(params_list),
        )
        session = self._get_session()
        enm_cmd = session.command()
        response = enm_cmd.execute(cmedit_get_command)
        self._close_session(session)

        return EnmData(
            cmd_output=response.get_output(),
            last_parameter=self._get_last_parameter(params_list),
        )

    def _get_scope(self) -> str:
        """Get scope of BSC for cli commands."""
        return ';'.join(self.bsc_set)
