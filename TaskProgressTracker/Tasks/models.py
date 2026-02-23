from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=150, blank=False)
    description = models.CharField(blank=False, max_length=500)
    target_min = models.IntegerField(default=1)
    target_max = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def latest_progress(self):
        return self.progress_entries.order_by('-created_at').first()
    
    
class ProgressEntry(models.Model):
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,
        related_name='progress_entries'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField()
    note = models.CharField(blank=False, default='No Comments', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    progress_value = models.IntegerField()

    class Meta:
        ordering = ['created_at']


class TaskStatus(models.Model):
    class StatusChoices(models.TextChoices):
        TODO = 'TODO', 'To Do'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        BLOCKED = 'BLOCKED', 'Blocked'
        DONE = 'DONE', 'Done'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_status')
    status = models.CharField(max_length=20,choices=StatusChoices.choices, default=StatusChoices.TODO)
    updated_at = models.DateTimeField(auto_now=True)
