from django.urls import path

from .views.task_views import (
    CreateTaskAPI,
    GetTaskAPI,
    UpdateTargetMinAPI,
    UpdateTargetMaxAPI,
    UpdateTaskTitleAPI,
    UpdateTaskDescriptionAPI,
)

from .views.progress_views import (
    CreateProgressAPI,
    SetProgressValueAPI,
)

from .views.status_views import (
    GetTaskStatusAPI,
    UpdateTaskStatusAPI,
)

urlpatterns = [

    # ======================
    # TASK APIs
    # ======================

    # Create a new task
    path(
        'api/v1/tasks/',
        CreateTaskAPI.as_view(),
        name='create-task'
    ),

    # Get a single task
    path(
        'api/v1/tasks/<int:task_id>/',
        GetTaskAPI.as_view(),
        name='get-task'
    ),

    # Update task target min
    path(
        'api/v1/tasks/<int:task_id>/target-min/',
        UpdateTargetMinAPI.as_view(),
        name='update-target-min'
    ),

    # Update task target max
    path(
        'api/v1/tasks/<int:task_id>/target-max/',
        UpdateTargetMaxAPI.as_view(),
        name='update-target-max'
    ),

    # Update task title
    path(
        'api/v1/tasks/<int:task_id>/title/',
        UpdateTaskTitleAPI.as_view(),
        name='update-task-title'
    ),

    # Update task description
    path(
        'api/v1/tasks/<int:task_id>/description/',
        UpdateTaskDescriptionAPI.as_view(),
        name='update-task-description'
    ),

    # ======================
    # PROGRESS APIs
    # ======================

    # Create progress entry (percentage, note, progress_value)
    path(
        'api/v1/progress/',
        CreateProgressAPI.as_view(),
        name='create-progress'
    ),

    # Set / validate progress value
    path(
        'api/v1/progress/set-value/',
        SetProgressValueAPI.as_view(),
        name='set-progress-value'
    ),

    # ======================
    # STATUS APIs
    # ======================

    # Get latest task status
    path(
        'api/v1/tasks/<int:task_id>/status/',
        GetTaskStatusAPI.as_view(),
        name='get-task-status'
    ),

    # Update task status
    path(
        'api/v1/tasks/<int:task_id>/status/update/',
        UpdateTaskStatusAPI.as_view(),
        name='update-task-status'
    ),
]
