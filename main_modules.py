import xml.etree.ElementTree as ET
from os.path import join
import json
from json import JSONEncoder

rootlist = []
rootname = 'Dispatcher'
moduledict = {}


class mytree:
    rootname = ''
    childs = []

    def __init__(self, rootname, childs):
        self.rootname = rootname
        self.childs = childs


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def treeParser(projectname):
    tree = ET.parse('/Users/oredata/Desktop/ivr_architecture/workspace/' + projectname + '/data/project.module')
    root = tree.getroot()
    return root


def parseDependencies(root, rootname):
    rootlist.append(rootname)
    t = dependencyfinder(root, rootname)
    moduledict[rootname] = t
    rootlist.remove(rootname)
    return t


def dependencyfinder(root, rootname):
    t = mytree(rootname, [])
    for child in root.find('.//dependencies'):
        if (child.tag == 'moduleref'):
            childname = child.get('name')
            if (childname not in rootlist):
                # print(childname)
                if (childname not in moduledict.keys()):
                    childtree = parseDependencies(treeParser(childname), childname)
                else:
                    childtree = moduledict.get(childname)
                t.childs.append(childtree)
    return t

def writeToFile(text):
    text = text.replace('rootname', 'text').replace('childs', 'nodes')
    parsed = json.loads(text)
    parsed = json.dumps(parsed, indent=4)
    print('Creating a new file')
    path = "/Users/oredata/Desktop"
    name = 'bilge' + '.json'  # Name of text file coerced with +.txt

    try:
        file = open(join(path, name), 'w')  # Trying to create a new file or open one
        file.write(parsed)
        file.close()

    except:
        print('Bir Hata Oluştu')
