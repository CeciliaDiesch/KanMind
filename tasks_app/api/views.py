from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db.models import Q
from ..models import Task, Comment
from boards_app.models import Board
from .serializers import TaskSerializer, CommentSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for creating, listing, retrieving, updating and deleting tasks."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks belonging to boards the current user is a member of."""
        user = self.request.user
        return Task.objects.filter(
            Q(board__owner=user) | Q(board__members=user)
        ).distinct()

    def get_object(self):
        """Retrieve task by pk, raising 404 if not found or 403 if not a member."""
        try:
            task = Task.objects.get(pk=self.kwargs['pk'])
        except Task.DoesNotExist:
            raise NotFound('Task nicht gefunden.')
        user = self.request.user
        if task.board.owner != user and not task.board.members.filter(
                pk=user.pk).exists():
            raise PermissionDenied('Du bist kein Mitglied dieses Boards.')
        return task

    @action(detail=False, methods=['get'], url_path='assigned-to-me')
    def assigned_to_me(self, request):
        """Return all tasks assigned to the current user."""
        tasks = Task.objects.filter(assignee=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='reviewing')
    def reviewing(self, request):
        """Return all tasks where the current user is the reviewer."""
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Verify board membership and save task with the current user as creator."""
        board = serializer.validated_data.get('board')
        user = self.request.user
        if board.owner != user and not board.members.filter(
                pk=user.pk).exists():
            raise PermissionDenied('Du bist kein Mitglied dieses Boards.')
        serializer.save(created_by=user)

    def partial_update(self, request, *args, **kwargs):
        """Update a task partially; board field cannot be changed."""
        request.data.pop('board', None)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete a task; only the creator or board owner is allowed."""
        task = self.get_object()
        user = request.user
        if task.created_by != user and task.board.owner != user:
            raise PermissionDenied(
                'Nur der Ersteller oder der Board-Eigentümer'
                ' kann diese Task löschen.')
        task.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        """List all comments for a task (GET) or add a new one (POST)."""
        task = self.get_object()
        if request.method == 'GET':
            comments = task.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True, methods=['delete'],
        url_path='comments/(?P<comment_id>[^/.]+)'
    )
    def delete_comment(self, request, pk=None, comment_id=None):
        """Delete a specific comment; only the author is allowed."""
        task = self.get_object()
        try:
            comment = Comment.objects.get(pk=comment_id, task=task)
        except Comment.DoesNotExist:
            raise NotFound('Kommentar nicht gefunden.')
        if comment.author != request.user:
            raise PermissionDenied(
                'Nur der Ersteller kann diesen Kommentar löschen.')
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
