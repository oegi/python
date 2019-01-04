from django.contrib import admin

from django.utils.translation import gettext_lazy as _


class Admin(admin.ModelAdmin):
    list_display = ('order_field','is_active','date_created','question', 'category',  'date_update')
    list_filter = ('question', 'answer', 'order_field')
    fieldsets = (
        (None, {'fields': ('question', 'answer', 'is_active')}),
        (_('Categories'), {'fields': ('category',)}),
        (_('Order'), {'fields': ('order_field',)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'question',
                'answer',
                'category',
                'is_active',
                'order_field'
            ),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
