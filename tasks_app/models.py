from django.db import models
from django.conf import settings
from boards_app.models import Board


class Task(models.Model):
    PRIO_CHOICES = [('low', 'low'), ('medium', 'medium'),
                    ('high', 'high'), ('urgent', 'urgent')]
    STATUS_CHOICES = [('to-do', 'to-do'), ('in-progress',
                                           'in-progress'), ('review', 'review'), ('done', 'done')]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(
        max_length=10, choices=PRIO_CHOICES, default='medium')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='to-do')

    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_tasks"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reviewed_tasks"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.task}'
