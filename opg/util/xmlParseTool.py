import xml.etree.ElementTree as ET


class Xml_Parserfile(object):
    '''
       xml 文件解析
    '''

    def __init__(self, filename):
        '''
               filename ： 要解析xml文件路径
        '''
        self.filename = filename

    def parserSql(self):
        tree = ET.parse(self.filename)  # 打开xml文档
        root = tree.getroot()
        # root = ET.fromstring(str(self.filename)) #从字符串传递xml
        for sqlnode in root.findall('mysql'):  # 找到root节点下的所有country节点
            name = sqlnode.find('name').text  # 子节点下节点rank的值
            opertype = sqlnode.find('opertype').text  # 子节点下节点rank的值
            sql = sqlnode.find('sql').text  # 子节点下节点rank的值
            townname = None
            townnameObj = sqlnode.find('townname')
            if townnameObj is not None:
                townname = townnameObj.text
            yield (name, opertype, sql, townname)

    def parser_method(self, xmlCont, fileName):
        tree = ET.fromstring(str(xmlCont))
        # The code below would need to be swapped for something specific to
        # what your looking for. Left here as an example.
        for child in tree.findall('Abbr'):
            sendMode = child.find('./SendConfiguration/AddressInfo/SendMode')
            if(sendMode.text == "Fax"):
                entryNum = child.find('AbbrNo').text
                entryName = child.find('Name').text
                faxNumber = child.find(
                    './SendConfiguration/AddressInfo/FaxMode/PhoneNumber')
                outputFile = open('result - %s' % fileName, 'a')
                outputFile.write(
                    "%s: %s , Type: %s , Number: %s  \n\n" %
                    (entryNum, entryName, sendMode.text, faxNumber.text))
                outputFile.close()

        print("Parsed " + fileName)

    def parseJmxFileTheardNum(self, name: object, newValue: object) -> object:
        tree = ET.parse(self.filename)  # 打开xml文档
        root = tree.getroot()
        threadNodeList = root.findall(
            "./hashTree/hashTree/ThreadGroup/stringProp")
        for theadNode in threadNodeList:
            tagname = theadNode.attrib['name']
            if tagname == name:
                theadNode.text = newValue
                ET.dump(theadNode)
                break
        ET.dump(root)
        tree.write(self.filename)

    def setThradNum(self, newValue):
        name = "ThreadGroup.num_threads"
        self.parseJmxFileTheardNum(name=name, newValue=newValue)


if __name__ == '__main__':
    xmll = Xml_Parserfile(
        filename="D:\\litaojun\\workspace\\steamJmeterScript\\jmeter\\script\\findPage.jmx")
    xmll.parseJmxFileTheardNum("ThreadGroup.num_threads", "200")
