'''
This script loads config files and parses them to provide necessary information for the 
automation flow.
'''
import configparser

REQUIRED_CONFIG_OPTIONS = [
    'server', 'account', 'password', 'max_messages'
]


class ConfigLoader:

    def __init__(self, config_files=None):
        self.config_list = []
        self._parse_config_file(config_files)

    def get_configs(self):
        return self.config_list

    def load_configs(self, config_files=None):
        self.config_list = []
        self._parse_config_file(config_files)
        return self.config_list

    def _parse_config_file(self, config_files):
        if not config_files:
            print('No config file was provided!')
            return None

        parser = configparser.RawConfigParser()
        sections = parser.sections()
        for section in sections:
            config_section = {
                'section': section
            }
            options = parser.options(section)
            for option in options:
                config_section[option] = parser.get(section=section, option=option)

            if self._validate_config_section(config_section):
                self.config_list.append(config_section)

    def _validate_config_section(self, config_section):
        if all(option in config_section for option in REQUIRED_CONFIG_OPTIONS):
            return True
        print(f"Config section {config_section['section']} is missing required options.")
        return False
