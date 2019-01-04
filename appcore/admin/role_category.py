from django.contrib import admin

from django.utils.translation import gettext_lazy as _


class Admin(admin.ModelAdmin):
    list_display = ('role',  'category', 'date_created', 'date_update', 'is_active',)
    list_filter = ('role', 'category', 'date_created', 'date_update', 'is_active',)
    fieldsets = (
        (_('Roles'), {'fields': ('role',)}),
        (_('Categories'), {'fields': ('category',)}),
        (_('Activo'), {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'role',
                'category',
                'is_active',
            ),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        if db_field.name == 'menu':
            kwargs['queryset'] = Category.objects.filter(title='Aplicaciones')
        """
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
