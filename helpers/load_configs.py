'''
This script loads config files and parses them to provide necessary information for the 
automation flow.
'''
import configparser


class ConfigLoader:

    def __init__(self, config_file=None):
        self.config_list = []
        self._parse_config_file(config_file)

    def _parse_config_file(self, config_file):
        if not config_file:
            print('No config file was provided!')
            return None

        parser = configparser.RawConfigParser()
        print(parser.read(config_file))
        sections = parser.sections()
        for section in sections:
            print('Section: ', section)
            options = parser.options(section)
            print('Options: ', options)
            for option in options:
                print(f"{option}: {parser.get(section=section, option=option)}")
            print('*'*100)


if __name__=='__main__':
    loader = ConfigLoader(['configs/example.conf', 'configs/test.conf'])
