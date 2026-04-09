from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Task, Comment


class UserMiniSerializer(serializers.ModelSerializer):
    """Minimal user serializer exposing id, email and full name."""

    fullname = serializers.ReadOnlyField(source='first_name')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task list, create and update endpoints."""
    assignee = UserMiniSerializer(read_only=True)
    reviewer = UserMiniSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee',
        write_only=True, required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer',
        write_only=True, required=False, allow_null=True
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'assignee_id', 'reviewer', 'reviewer_id',
                  'due_date', 'comments_count']

    def get_comments_count(self, obj):
        """Return the total number of comments on this task."""
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for task comments."""
    author = serializers.ReadOnlyField(source='author.first_name')

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']
