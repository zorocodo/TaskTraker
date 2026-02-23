from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import Task, ProgressEntry
from ..serializers import TaskSerializer, ProgressEntrySerializer
from ..services.task_service import validate_target_range


# -----------------------------
# CREATE TASK
# -----------------------------
class CreateTaskAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(user=request.user)

        # Create initial progress
        ProgressEntry.objects.create(
            user=request.user,
            task=task,
            percentage=0,
            progress_value=0
        )

        # Re-serialize task to include any nested data
        final_serializer = TaskSerializer(task)
        return Response(final_serializer.data, status=status.HTTP_201_CREATED)


# -----------------------------
# GET SINGLE TASK
# -----------------------------
class GetTaskAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


# -----------------------------
# UPDATE TITLE
# -----------------------------
class UpdateTaskTitleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.title = request.data.get('title', task.title)
        task.save(update_fields=['title'])
        return Response({"message": "Title updated"})


# -----------------------------
# UPDATE DESCRIPTION
# -----------------------------
class UpdateTaskDescriptionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.description = request.data.get('description', task.description)
        task.save(update_fields=['description'])
        return Response({"message": "Description updated"})


# -----------------------------
# UPDATE TARGET MIN
# -----------------------------
class UpdateTargetMinAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        new_min = request.data.get('target_min', task.target_min)
        validate_target_range(new_min, task.target_max)
        task.target_min = new_min
        task.save(update_fields=['target_min'])
        return Response({"message": "Target min updated"})


# -----------------------------
# UPDATE TARGET MAX
# -----------------------------
class UpdateTargetMaxAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        new_max = request.data.get('target_max', task.target_max)
        validate_target_range(task.target_min, new_max)
        task.target_max = new_max
        task.save(update_fields=['target_max'])
        return Response({"message": "Target max updated"})


# -----------------------------
# DELETE TASK
# -----------------------------
class DeleteTaskAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        return Response({"message": "Task Deleted"}, status=status.HTTP_204_NO_CONTENT)


# -----------------------------
# LIST TASKS
# -----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list_create(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)