from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Task, ProgressEntry, TaskStatus
from .serializers import (
    TaskSerializer,
    ProgressEntrySerializer,
    TaskStatusSerializer
)


class CreateTaskAPI(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()

            # BUSINESS LOGIC:
            # create initial status automatically
            TaskStatus.objects.create(task=task)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTaskAPI(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


class CreateProgressEntryAPI(APIView):
    def post(self, request):
        serializer = ProgressEntrySerializer(data=request.data)
        if serializer.is_valid():
            # BUSINESS LOGIC:
            # validate percentage range (0–100)
            percentage = serializer.validated_data['percentage']
            if not 0 <= percentage <= 100:
                return Response(
                    {"error": "Percentage must be between 0 and 100"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetProgressValueAPI(APIView):
    def post(self, request):
        serializer = ProgressEntrySerializer(data=request.data)
        if serializer.is_valid():
            # BUSINESS LOGIC:
            # validate progress_value vs target_min/max
            task = serializer.validated_data['task']
            value = serializer.validated_data['progress_value']

            if not task.target_min <= value <= task.target_max:
                return Response(
                    {"error": "Progress value out of task target range"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class UpdateTaskStatusAPI(APIView):
    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        new_status = request.data.get('status')

        # BUSINESS LOGIC:
        # validate allowed transitions here later
        TaskStatus.objects.create(
            task=task,
            status=new_status
        )

        return Response({"message": "Status updated"})
