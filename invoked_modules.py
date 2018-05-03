import os
from pathlib import Path

hataliliste = []
denemelist = []


class invoked_module:
    java_name = ''
    java_path = ''
    module_name = ''
    node_name = ''

    def __init__(self, rootname, childs, modulename, node_name):
        self.rootname = rootname
        self.childs = childs
        self.module_name = modulename
        self.node_name = node_name


def func_traverse_path(path, modulename):
    try:
        directory = os.listdir(path)
        for fileinfolder in directory:
            pathoffile = path + '/' + fileinfolder
            my_file = Path(pathoffile)
            if (my_file.is_dir()):
                func_traverse_path(pathoffile, modulename)
            else:
                if (pathoffile.endswith('.java')):
                    a = open(pathoffile).read()
                    result = findifInvokerFromFile(a, fileinfolder, path)
                    if (result.java_name != ''):
                        denemelist.append(result)
    except Exception:
        hataliliste.append(modulename)


def findifInvokerFromFile(gelendata, filename, path):
    mywordlist = str(gelendata).split()
    result = invoked_module('', '', '', '')
    splittedpath = path.split('/WEB-INF/src/')
    originalpath = splittedpath[1]

    if 'extends' in mywordlist:
        indexExtends = mywordlist.index('extends')

        if (mywordlist[indexExtends + 1].split('.')[-1] == 'Invoke'):
            if (str(filename) != ''):
                result.java_name = str(filename)
                result.java_path = originalpath
                result.module_name = findModulaName(gelendata)
                if (result.module_name == 'AveaMenuLog'):
                    result.node_name = findNodeName(gelendata)

    return result


def findModulaName(gelendata):
    modulename = gelendata.split('return(checkEntryPoint(\"')[1].split('/Start')[0]
    return modulename


def findNodeName(gelendata):
    node_name = \
        gelendata.split('param = new com.avaya.sce.runtime.Parameter(\"nodeName\", \"')[1].split('\", com.avaya.sce')[0]
    return node_name
