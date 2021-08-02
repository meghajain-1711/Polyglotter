from configparser import ConfigParser


class MyException(Exception):
    pass


class MyConfig(ConfigParser):
    def __init__(self, config_file):
        super(MyConfig, self).__init__()

        self.read(config_file)
        self.validate_config()

    def id_dict(self,obj):
        return obj.__class__.__name__ == 'dict'

    def contains_key_rec(self,v_key, v_dict):
        for curKey in v_dict:
            if curKey == v_key or (id_dict(v_dict[curKey]) and contains_key_rec(v_key, v_dict[curKey])):
                return True
        return False

    def load_doc(self,file):
        with open(file, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exception:
            raise exception 

    def recursive_nested_key(self,dictionary):
        for key, value in dictionary.items():
            if self.id_dict(value):
            yield from self.recursive_nested_key(value)
            else:
            yield (key,value)

    def validate_config(self,schema_file,config_file):
        conf=self.load_doc(self.config_file)
        schem=self.load_doc(schema_file)
        for key,val in self.recursive_nested_key(schem):  
            if self.contains_key_rec(key, conf):
            print("key {} exists in config file".format(key))
            else:
            print("key {} does not exist in config file".format(key))
            return 0
        return 1
    

