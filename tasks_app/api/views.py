from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    Zuständig für alle Task-Operationen (Checkliste: Ressourcenorientiert).
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.all()

        # Filter-Logik für dashboard.js (assigned vs reviewer)
        assigned_only = self.request.query_param.get('assigned')
        if assigned_only:
            queryset = queryset.filter(assignee=user)

        reviewer_only = self.request.query_param.get('reviewer')
        if reviewer_only:
            queryset = queryset.filter(reviewer=user)

        # Filter für board.js (alle Tasks eines bestimmten Boards)
        board_id = self.request.query_param.get('board')
        if board_id:
            queryset = queryset.filter(board_id=board_id)

        return queryset
