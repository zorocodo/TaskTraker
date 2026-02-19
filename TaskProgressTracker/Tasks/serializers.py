from rest_framework import serializers
from .models import Task, ProgressEntry, TaskStatus


class TaskSerializer(serializers.ModelSerializer):
    current_progress = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_current_progress(self, obj):
        latest = obj.latest_progress()
        return latest.percentage if latest else 0


class ProgressEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressEntry
        fields = '__all__'


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'
