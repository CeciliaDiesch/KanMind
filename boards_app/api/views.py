from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from ..models import Board
# Serializer erstellen wir als Nächstes
from .serializers import BoardSerializer


class BoardViewSet(viewsets.ModelViewSet):
    """
    Handhabt CRUD für Boards (Checkliste: ModelViewSet verwenden).
    """
    serializer_class = BoardSerializer  # (many=True)
    permission_classes = [IsAuthenticated]  # IsStaffOrReadOnly

    def get_queryset(self):
        # Zeige nur Boards an, bei denen der User Owner oder Mitglied ist (für dashboard.js)
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        # Setzt den Ersteller automatisch als Owner (Clean Code Prinzip)
        serializer.save(owner=self.request.user)
