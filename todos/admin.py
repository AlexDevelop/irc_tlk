from django.contrib import admin
from todos.models import TodoList, TodoType


class TodoListAdmin(admin.ModelAdmin):
    pass


class TodoTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(TodoType, TodoTypeAdmin)
admin.site.register(TodoList, TodoListAdmin)