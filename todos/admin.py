from django.contrib import admin
from todos.models import TodoList, TodoType, Setting, SettingData


class TodoListAdmin(admin.ModelAdmin):
    list_filter = ('created', 'status', )
    ordering = ('-created', )
    list_display = ('status', 'created', 'identifier', 'todo_type_id', )


class TodoTypeAdmin(admin.ModelAdmin):
    pass


class SettingAdmin(admin.ModelAdmin):
    pass

class SettingDataAdmin(admin.ModelAdmin):
    pass

admin.site.register(TodoType, TodoTypeAdmin)
admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(SettingData, SettingDataAdmin)

