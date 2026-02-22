from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Task, TaskStatus
from ..services.status_service import validate_status_transition
from ..serializers import TaskStatusSerializer

class UpdateTaskStatusAPI(APIView):
    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        latest = task.task_status.order_by('-updated_at').first()
        new_status = request.data['status']

        validate_status_transition(latest.status, new_status)

        TaskStatus.objects.create(task=task, status=new_status)
        return Response({"message": "Status updated"})

class GetTaskStatusAPI(APIView):
    def get(self, request, task_id):
        status_obj = (
            TaskStatus.objects
            .filter(task_id=task_id)
            .order_by('-updated_at')
            .first()
        )
        serializer = TaskStatusSerializer(status_obj)
        return Response(serializer.data)

class CreateTaskStatusAPI(APIView):
    def post(self, request, task_id):
        task = Task.objects.get(id = task_id)
        task_status_data = request.data['status']
        task_status_obj = TaskStatus.objects.create(task = task, status= task_status_data)
        serializer = TaskStatusSerializer(task_status_obj)
        return Response(serializer.data)

