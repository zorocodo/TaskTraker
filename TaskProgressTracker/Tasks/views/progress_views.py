from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import ProgressEntry, Task
from ..serializers import ProgressEntrySerializer
from ..services.progress_service import validate_percentage


# -----------------------------
# CREATE PROGRESS ENTRY
# -----------------------------
class CreateProgressAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProgressEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Ensure user owns the task
        task = get_object_or_404(Task, id=serializer.validated_data['task'].id, user=request.user)

        # Validate percentage
        validate_percentage(serializer.validated_data['percentage'])

        # Save progress entry with user
        serializer.save(user=request.user, task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -----------------------------
# SET PROGRESS VALUE (with target range validation)
# -----------------------------
class SetProgressValueAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProgressEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = get_object_or_404(Task, id=serializer.validated_data['task'].id, user=request.user)
        value = serializer.validated_data['progress_value']

        # Check if value is within task range
        if not task.target_min <= value <= task.target_max:
            return Response(
                {"error": "Progress value out of task target range"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save progress entry
        serializer.save(user=request.user, task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)