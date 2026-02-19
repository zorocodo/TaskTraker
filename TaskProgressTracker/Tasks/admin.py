from django.contrib import admin

# Register your models here.
from .models import Task, ProgressEntry, TaskStatus

admin.site.register(Task)
admin.site.register(ProgressEntry)
admin.site.register(TaskStatus)
