from django.urls import path

from .views.task_views import (
    CreateTaskAPI,
    GetTaskAPI,
    UpdateTargetMinAPI,
    UpdateTargetMaxAPI,
    UpdateTaskTitleAPI,
    UpdateTaskDescriptionAPI,
    task_list_create,
    DeleteTaskAPI,
)

from .views.progress_views import (
    CreateProgressAPI,
    SetProgressValueAPI,
)

from .views.status_views import (
    GetTaskStatusAPI,
    UpdateTaskStatusAPI,
    CreateTaskStatusAPI,
)

from .views.user_views import (
    RegisterAPI,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/v1/register/', RegisterAPI.as_view(), name='register'),

    path('api/v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/tasks/', task_list_create, name='task-list-create'),
    path('api/v1/tasks/create/', CreateTaskAPI.as_view(), name='create-task'),
    path('api/v1/tasks/<int:task_id>/', GetTaskAPI.as_view(), name='get-task'),

    path('api/v1/tasks/<int:task_id>/target-min/', UpdateTargetMinAPI.as_view()),
    path('api/v1/tasks/<int:task_id>/target-max/', UpdateTargetMaxAPI.as_view()),
    path('api/v1/tasks/<int:task_id>/title/', UpdateTaskTitleAPI.as_view()),
    path('api/v1/tasks/<int:task_id>/description/', UpdateTaskDescriptionAPI.as_view()),

    path('api/v1/progress/', CreateProgressAPI.as_view()),
    path('api/v1/progress/set-value/', SetProgressValueAPI.as_view()),

    path('api/v1/tasks/<int:task_id>/delete/', DeleteTaskAPI.as_view()),

    path('api/v1/tasks/<int:task_id>/status/', GetTaskStatusAPI.as_view()),
    path('api/v1/tasks/<int:task_id>/status/update/', UpdateTaskStatusAPI.as_view()),
    path('api/v1/tasks/<int:task_id>/status/create/', CreateTaskStatusAPI.as_view()),
]
