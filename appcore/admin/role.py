from django.contrib import admin


class Admin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'date_created', 'date_update', 'is_active',)
