import string
from pathlib import Path
from typing import Dict, List

from services.enm.enmscripting import EnmScripting

TEMPLATES_PATH = 'enm_api/templates'


class EnmCli(EnmScripting):
    """A class for communicating with ENM CLI for object creation."""

    templates = {
        'COM': f'{TEMPLATES_PATH}/create_object_com.txt',
        'CPP': f'{TEMPLATES_PATH}/create_object_cpp.txt',
        'XML': f'{TEMPLATES_PATH}/com.xml',
    }

    def create_object(self, object_data: dict) -> None:
        """Create Base Station object on ENM."""
        ne_type = self._determine_ne_type(object_data['platform'], object_data['technologies'])
        template = self._get_template(object_data['platform'])
        commands = self._generate_object_commands(
            template,
            subnetwork=object_data['subnetwork'],
            sitename=object_data['sitename'],
            oam_ip=object_data['oam_ip'],
            ne_type=ne_type,
        )
        session = self._get_session()
        terminal = session.terminal()
        for command in commands:
            terminal.execute(command)
        self._close_session(session)

    def load_xml(self, sitename: str, enm: str) -> None:
        """Load XML for new Base Station object."""
        xml_path = self._generate_xml(sitename, enm)
        command = 'pkiadm etm -c -xf file:{xml}'.format(xml=Path(xml_path).name)

        session = self._get_session()
        terminal = session.terminal()
        with open(xml_path, 'r') as xml:
            terminal.execute(command, xml)
        self._close_session(session)
        Path(xml_path).unlink()

    def set_controller(self, technology: str, sitename: str, controller: str) -> None:
        """Set controller for Base Station."""
        commands = {
            'GSM': (
                f'cmedit set NetworkElement={sitename} '
                f'controllingBsc=NetworkElement={controller}'
            ),
            'UMTS': (
                f'cmedit set NetworkElement={sitename} '
                f'controllingRnc=NetworkElement={controller}'
            ),
        }
        session = self._get_session()
        terminal = session.terminal()
        terminal.execute(commands[technology])
        self._close_session(session)

    def get_object_info(self, sitename: str) -> Dict[str, str]:
        """Get information about Base Station object."""
        command = f'cmedit get NetworkElement={sitename}'
        session = self._get_session()
        terminal = session.terminal()
        object_info = terminal.execute(command)
        self._close_session(session)
        return object_info.get_output()

    def _determine_ne_type(self, platform: str, technologies: List[str]) -> str:
        """Determine neType."""
        if platform == 'COM':
            return 'RadioNode'
        if 'LTE' in technologies:
            return 'ERBS'
        return 'RBS'

    def _get_template(self, temp_type: str) -> str:
        """Get template path."""
        return self.templates[temp_type]

    def _generate_object_commands(self, template: str, **kwargs) -> List[str]:
        """Generate ENM CLI commands for object creation."""
        commands = []
        with open(template, 'r') as temp:
            rows = temp.readlines()

        for row in rows:
            temp_command = string.Template(row)
            command = temp_command.safe_substitute(**kwargs)
            commands.append(command.rstrip())
        return commands

    def _generate_xml(self, sitename: str, enm: str) -> str:
        """Generate XML from template."""
        with open(self._get_template('XML')) as temp:
            rows = temp.readlines()

        xml_path = f'{TEMPLATES_PATH}/{sitename}.xml'
        with open(xml_path, 'w') as xml:
            for row in rows:
                temp_row = string.Template(row)
                xml_row = temp_row.safe_substitute(sitename=sitename, enm=enm)
                xml.write(xml_row)
        return xml_path
