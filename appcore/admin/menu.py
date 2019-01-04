from django.contrib import admin

from django.utils.translation import gettext_lazy as _

class Admin(admin.ModelAdmin):
    list_display = ('order_field','title', 'date_created', 'date_update','is_active',)
    list_filter = ('title','is_active',)
    fieldsets = (
        (None, {'fields': ('title', 'is_active', )}),
        (_('Imagen'), {'fields': ('content_rich',)}),
        (_('Order'), {'fields': ('order_field',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'title',
                'content_rich',
                'is_active',
                'order_field'
            ),
        }),
    )

    def get_queryset(self, request):
        qs = super(Admin, self).get_queryset(request).order_by('order_field')
        return qs

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
