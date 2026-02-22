from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import ProgressEntrySerializer
from ..services.progress_service import validate_percentage


class CreateProgressAPI(APIView):
    def post(self, request):
        serializer = ProgressEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_percentage(serializer.validated_data['percentage'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
