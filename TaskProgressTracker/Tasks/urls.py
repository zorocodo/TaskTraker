from django.urls import path
from .views import *

urlpatterns = [
    path('task/create/', CreateTaskAPI.as_view()),
    path('task/<int:task_id>/', GetTaskAPI.as_view()),

    path('progress/create/', CreateProgressEntryAPI.as_view()),
    path('progress/set-value/', SetProgressValueAPI.as_view()),

    path('task/<int:task_id>/target-min/', UpdateTargetMinAPI.as_view()),
    path('task/<int:task_id>/target-max/', UpdateTargetMaxAPI.as_view()),
    path('task/<int:task_id>/title/', UpdateTaskTitleAPI.as_view()),
    path('task/<int:task_id>/description/', UpdateTaskDescriptionAPI.as_view()),

    path('task/<int:task_id>/status/', GetTaskStatusAPI.as_view()),
    path('task/<int:task_id>/status/update/', UpdateTaskStatusAPI.as_view()),
]
