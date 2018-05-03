import main_modules as mm
from invoked_modules import *

result = mm.parseDependencies(mm.treeParser(mm.rootname), mm.rootname)
text = mm.MyEncoder().encode(mm.moduledict['Dispatcher'])
mm.writeToFile(text)

# burdan calıstırıyoruz

for dispatcherchilds in mm.moduledict['Dispatcher'].childs:
    modulename = dispatcherchilds.rootname
    print(modulename)
    path = '/Users/oredata/Desktop/ivr_architecture/workspace/' + modulename + '/WEB-INF/src/flow'
    func_traverse_path(path, modulename)

i = 1
for x in denemelist:
    print(str(i) + '.')
    print('Java Name: ' + x.java_name)
    print('Java Path: ' + x.java_path)
    print('module name: ' + x.module_name)
    if x.node_name != '':
        print('node name: ' + x.node_name)
    i = i + 1
