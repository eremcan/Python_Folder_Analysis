import main_modules as mm
from invoked_modules import *

result = mm.parseDependencies(mm.treeParser(mm.rootname), mm.rootname)
text = mm.MyEncoder().encode(mm.moduledict['Dispatcher'])
mm.writeToFile(text)

dependencyDict = {}

def traverse_dictionary(keystr,m,requestedChild):
    its_instance = invoked_tree_structure(keystr,m,[])
    for child in mm.moduledict[keystr].childs:

        modulename = child.rootname
        if(modulename != requestedChild and requestedChild != ''):
            continue
       # print("Start Module : "+modulename)
        path = '/Users/oredata/Desktop/ivr_architecture/workspace/' + modulename + '/WEB-INF/src/flow'
        if(modulename not in dependencyDict.keys()):
            if(modulename == 'KK_LiraYukleme'):
                print('emin')
            moduledependencylist =  func_traverse_path(path, modulename)
            moduledependencylist = getDecreasedModuleList(moduledependencylist)
        else:
            moduledependencylist = dependencyDict[modulename]
        if(len(child.childs)> 0):
            dependencyDict[modulename]=moduledependencylist
        its_instance.childs.append(traverse_dictionary(modulename,moduledependencylist,''))

       # print("End Module : " + modulename)
    return its_instance

def debugall():
    #its = traverse_dictionary('Postpaid_500_Menu_ve_AltMenuler', [])
    its = traverse_dictionary('Dispatcher', [], 'Postpaid_500_Menu_ve_AltMenuler')
    print(its)
    invokedfiletojson(its)



debugall()


