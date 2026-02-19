from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Task
from ..serializers import TaskSerializer
from ..services.task_service import validate_target_range


class CreateTaskAPI(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateTargetMinAPI(APIView):
    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        new_min = request.data['target_min']
        validate_target_range(new_min, task.target_max)
        task.target_min = new_min
        task.save(update_fields=['target_min'])
        return Response({"message": "target_min updated"})


class GetTaskAPI(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


class UpdateTargetMinAPI(APIView):
    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.target_min = request.data.get('target_min', task.target_min)
        task.save(update_fields=['target_min'])
        return Response({"message": "Target min updated"})


class UpdateTargetMaxAPI(APIView):
    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.target_max = request.data.get('target_max', task.target_max)
        task.save(update_fields=['target_max'])
        return Response({"message": "Target max updated"})


class UpdateTaskTitleAPI(APIView):
    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.title = request.data.get('title', task.title)
        task.save(update_fields=['title'])
        return Response({"message": "Title updated"})


class UpdateTaskDescriptionAPI(APIView):
    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.description = request.data.get('description', task.description)
        task.save(update_fields=['description'])
        return Response({"message": "Description updated"})


@api_view(['GET', 'POST'])
def task_list_create(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
