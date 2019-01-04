from django.contrib import admin

from django.utils.translation import gettext_lazy as _


class Admin(admin.ModelAdmin):
    list_display = ('title', 'menu',  'date_created', 'date_update', 'path_file', 'is_active',)
    list_filter = ('title', 'menu',  'is_active',)
    fieldsets = (
        (None, {'fields': ('title', 'is_active',)}),
        (_('Menus'), {'fields': ('menu',)}),
        (_('Enlace Aplicaciones'), {'fields': ('content_rich',)}),
        (_('Path File'), {'fields': ('path_file',)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'title',
                'menu',
                'content_rich',
                'path_file',
                'is_active',

            ),
        }),
    )

    def get_queryset(self, request):
        qs = super(Admin, self).get_queryset(request).order_by('menu__title')
        return qs

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
