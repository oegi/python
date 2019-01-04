import glob
import os
import sys
from builtins import print
from collections import defaultdict

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

# los modelo deben ir despues del django.setup()

os.path.exists('/SOCKET/')

print("************INICIO************")

level = 0
if os.path.exists('/SOCKET/'):
    todos = glob.glob('/SOCKET/*')
    directorios = []
    archivos = []
    tree = []
    parents = []
    cont = 0
    for base, dirs, files in os.walk('/SOCKET/'):
        directorios.append({
            "base": base,
            "dirs": dirs,
            "files": files,
        })


        longdirs = len(dirs)
        longfiles = len(files)
        if level == 0:

            tree.append({
                "parent": "#",
                "id": base,
                "text": base,
                "icon": "fa fa-folder",

            })
            parents.append(base)
        for d in range(longdirs):
            cont += 1
            tree.append({
                "parent": base,
                #"idparent": parents,
                "id": cont,
                "text": dirs[d],
                "icon": "fa fa-folder",

            })
            parents.append(dirs[d])

        for k in range(longfiles):
            cont += 1
            parent = base
            tree.append({
                "parent": base,
                "id": base,
                #"idparent": parents,
                "text": files[k],
                "icon": "far fa-file-alt",

            })
            parents.append(files[k])




        level += 1
        print("level", level)





print(tree)
print("lista: ",parents)
print(parents.index('SOCKET_20181219.xlsx'))
print("************FIN************")
