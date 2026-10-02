'''
This script loads config files and parses them to provide necessary information for the 
automation flow.
'''
import configparser

REQUIRED_CONFIG_OPTIONS = [
    'server', 'email', 'password', 'max_messages'
]


class ConfigLoader:

    def __init__(self):
        self.config_list = []
        self.parser = configparser.RawConfigParser()

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

        self.parser.read(config_files)
        sections = self.parser.sections()
        for section in sections:
            # print('Section: ', section)
            config_section = {
                'section': section
            }
            options = self.parser.options(section)
            # print('Options: ', options)
            for option in options:
                config_section[option] = self.parser.get(section=section, option=option)

            if self._validate_config_section(config_section):
                self.config_list.append(config_section)

            # print('Config section: ', config_section)
            # print('*'*100)

    def _validate_config_section(self, config_section):
        if all(option in config_section for option in REQUIRED_CONFIG_OPTIONS):
            return True
        print(f"Config section {config_section['section']} is missing required options.")
        return False
