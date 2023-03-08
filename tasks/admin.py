from django.contrib import admin

from .models import *


class PriorityAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )


class StageAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )
    

class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'description',
        'stage',
        'worker',
    )
    search_fields = ('description',)
    empty_value_display = '-пусто-'
    list_filter = ('title',)

admin.site.register(Priority, PriorityAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Task, TaskAdmin)

