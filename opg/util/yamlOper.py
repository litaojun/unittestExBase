from ruamel import yaml

#写json数据为YAML格式文件
def dumpDataToYmlFile(filePath = None,data = None):
    with open(filePath, 'w', encoding="utf-8") as f:
         yaml.dump(data,f,Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True)


def readYmlFile(filePath = None):
    with open(filePath, 'r', encoding="utf-8") as f:
        return yaml.load(f.read(),Loader=yaml.Loader)