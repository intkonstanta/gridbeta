from django.contrib import admin
from .models import user_project, all_tips

@admin.register(user_project)
class user_project_admin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'size', 'date', 'description',  'file',)
    list_filter = ('creator', 'size', 'date',)

    fieldsets = (
        (None, {
            'fields': ('creator', 'title', 'size', 'date', 'description',  'file',)
        }),
    )

@admin.register(all_tips)
class all_tips_admin(admin.ModelAdmin):
    list_display = ('title', 'text', 'img',)
    list_filter = ('title',)

    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'img',)
        }),
    )