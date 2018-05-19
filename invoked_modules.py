import os
from pathlib import Path
from os.path import join
import json
from json import JSONEncoder

hataliliste = []
invoked_module_dict = {}

class invoked_tree_structure:
    rootname = ''
    moduledependencylist = []
    childs = []

    def __init__(self,rootname,moduledependencylist,childs):
        self.rootname = rootname
        self.moduledependencylist = moduledependencylist
        self.childs = childs

class invoked_module:
    java_name = ''
    java_path = ''
    module_name = ''
    node_name = ''

    def __init__(self, javaname,javapath, modulename, nodename):
        self.java_name = javaname
        self.java_path = javapath
        self.module_name = modulename
        self.node_name = nodename


def func_traverse_path(path, modulename):
    invokedmodulelist = []
    try:
        directory = os.listdir(path)
        for fileinfolder in directory:
            pathoffile = path + '/' + fileinfolder
            my_file = Path(pathoffile)
            if (my_file.is_dir()):
                lst = func_traverse_path(pathoffile, modulename)
                if(len(lst)>0):
                    for l in lst:
                        invokedmodulelist.append(l)
            else:
                if (pathoffile.endswith('.java')):
                    a = open(pathoffile).read()
                    result = findifInvokerFromFile(a, fileinfolder, path)
                    if (result.java_name != ''):
                        invokedmodulelist.append(result)

        return invokedmodulelist

    except Exception:
        hataliliste.append(modulename)


def findifInvokerFromFile(gelendata, filename, path):
    if(filename == 'AveaPaymentNew1.java'):
        print('hatageliyor.')
    mywordlist = str(gelendata).split()
    result = invoked_module('', '', '', '')
    splittedpath = path.split('/WEB-INF/src/')
    originalpath = splittedpath[1]

    if 'extends' in mywordlist:
        indexExtends = mywordlist.index('extends')

        if (mywordlist[indexExtends + 1].split('.')[-1] == 'Invoke'):
            if (str(filename) != ''):
                result.java_name = filename
                result.java_path = originalpath
                result.module_name = findModuleName(gelendata)
                if (result.module_name == 'AveaMenuLog'):
                    result.node_name = findNodeName(gelendata)

    return result


def findModuleName(gelendata):

    modulename = gelendata.split('return(checkEntryPoint(\"')[1].split('/Start')[0]
    return modulename


def findNodeName(gelendata):

    node_name = \
        gelendata.split('param = new com.avaya.sce.runtime.Parameter(\"nodeName\", \"')[1].split('\", com.avaya.sce')[0]
    if(node_name == 'tmpLogData:nodeName'):
        print('hatanode')
    return node_name

def getDecreasedModuleList(moduledependencylist):
    resultDict = {}
    result = []
    try:
        for l in moduledependencylist:
            modulename = l.module_name
            if(modulename not in resultDict):
                resultDict[modulename] = l
            else:
                temp = resultDict[modulename]
                if(l.node_name == 'tmpLogData:nodeName'):
                    print("hata")
                temp.node_name = temp.node_name+','+l.node_name
                temp.java_name = temp.java_name + ',' + l.java_name
                temp.java_path = temp.java_path + ',' + l.java_path
                resultDict[modulename] = temp
        for k in resultDict.keys():
            result.append(resultDict[k])
        return result
    except :
        print('hata oldu.')



class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def invokedfiletojson(gelendata):
    seriliazedencodeddata = MyEncoder().encode(gelendata)
    parsed = json.loads(seriliazedencodeddata)
    parsed = json.dumps(parsed, indent=4,ensure_ascii=False)
    print('Creating a new file')
    path = "/Users/oredata/Desktop"
    name = 'deneme1' + '.json'  # Name of text file coerced with +.txt

    try:
        file = open(join(path, name), 'w')  # Trying to create a new file or open one
        file.write(parsed)
        file.close()

    except:
        print('Bir Hata Oluştu')



