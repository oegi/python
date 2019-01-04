from django.contrib import admin

from django.utils.translation import gettext_lazy as _


class Admin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_created', 'date_update','is_active',)
    list_filter = ('title', 'category','is_active')
    fieldsets = (
        (None, {'fields': ('title', 'description','is_active',)}),
        (_('Categories'), {'fields': ('category',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'title',
                'description',
                'category',
                'is_active',
            ),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
