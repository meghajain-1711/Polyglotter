from configparser import ConfigParser


class MyException(Exception):
    pass


class MyConfig(ConfigParser):
    def __init__(self, config_file):
        super(MyConfig, self).__init__()

        self.read(config_file)
        self.validate_config()

    def validate_config(self,schema_file):
        
        required_values = eval(open(schema_file, 'r').read())

        for section, keys in required_values.items():
            if section not in self:
                raise MyException(
                    'Missing section %s in the config file' % section)

            for key, values in keys.items():
                if key not in self[section] or self[section][key] == '':
                    raise MyException((
                        'Missing value for %s under section %s in ' +
                        'the config file') % (key, section))

                if values:
                    if self[section][key] not in values:
                        raise MyException((
                            'Invalid value for %s under section %s in ' +
                            'the config file') % (key, section))

cfg = {}

try:
    # The example config file has an invalid value so cfg will stay empty first
    cfg = MyConfig('example_config.yaml')
except MyException as e:
    # Initially you'll see this due to the invalid value
    print(e)
else:
    # Once you fix the config file you'll see this
    print(cfg['client']['fallback'])