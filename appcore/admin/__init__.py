from django.contrib import admin
from django.contrib.auth.models import Group

from appcore import models as model
from appcore.admin import (
    menu,
    category,
    content,
    question,
    user,
    role,
    role_menu,
    role_category,
)

# REGISTER

admin.site.register(model.Menu, menu.Admin)
admin.site.register(model.Category, category.Admin)
admin.site.register(model.Content, content.Admin)
admin.site.register(model.Questions, question.Admin)
admin.site.register(model.User, user.Admin)
admin.site.register(model.Role, role.Admin)
admin.site.register(model.RoleMenu, role_menu.Admin)
admin.site.register(model.RoleCategory, role_category.Admin)

# UN REGISTER
admin.site.unregister(Group)
