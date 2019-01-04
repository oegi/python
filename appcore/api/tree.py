import json
import os

from django.http import HttpResponse
from django.views.generic import View


class IndexView(View):
    http_method_names = ['post']

    @staticmethod
    def post(request, *args, **kwargs):
        data = json.loads(request.body)

        level = 0
        tree = []
        parents = []

        path = data.get('path')
        if os.path.exists(path):
            cont = 0

            for base, dirs, files in os.walk(path):
                id = cont
                longdirs = len(dirs)
                longfiles = len(files)
                parent = base.split("/")
                cantidad = len(parent)
                if level == 0:
                    tree.append({
                        "parent": "#",
                        "id": "index_" + str(cont),
                        "text": base,
                        "icon": "fa fa-folder",

                    })

                    parents.append(parent[cantidad - 1])

                for d in range(longdirs):
                    cont += 1
                    tree.append({
                        "parent": "index_" + str(parents.index(parent[cantidad - 1])),
                        "id": "index_" + str(cont),
                        "text": dirs[d],
                        "icon": "fa fa-folder",

                    })
                    parents.append(dirs[d])

                for k in range(longfiles):
                    cont += 1
                    tree.append({
                        "parent": "index_" + str(parents.index(parent[cantidad - 1])),
                        "id": "index_" + str(cont),
                        "text": files[k],
                        "icon": "far fa-file-alt",
                        "data": {
                            "id": "root.id",
                            "href": '/download/?file_name={}&directory={}'.format(files[k], base)
                        },
                    })
                    parents.append(files[k])

                level += 1

        return HttpResponse(json.dumps(
            dict(data=tree)
        ), content_type='application/json')
