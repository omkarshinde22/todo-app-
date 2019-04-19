from import_export import resources
from .models import TodoList

class Todo(resources.ModelResource):
    class Meta:
        model = TodoList
