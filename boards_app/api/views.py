from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db.models import Q
from django.contrib.auth.models import User
from ..models import Board
from .serializers import (
    BoardSerializer, BoardDetailSerializer, BoardPatchSerializer
)
from tasks_app.api.serializers import UserMiniSerializer
from core.permissions import check_board_member


class BoardViewSet(viewsets.ModelViewSet):
    """ViewSet for creating, listing, retrieving, updating and deleting boards."""

    serializer_class = BoardSerializer

    def get_queryset(self):
        """Return boards where the current user is owner or member."""

        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def get_serializer_class(self):
        """Return the appropriate serializer depending on the action."""

        if self.action == 'retrieve':
            return BoardDetailSerializer
        if self.action in ('update', 'partial_update'):
            return BoardPatchSerializer

        return BoardSerializer

    def get_object(self):
        """Retrieve board by pk, raising 404 if not found or 403 if not a member."""

        try:
            board = Board.objects.get(pk=self.kwargs['pk'])
        except Board.DoesNotExist:
            raise NotFound('Board nicht gefunden.')
        user = self.request.user
        check_board_member(user, board)

        return board

    def perform_create(self, serializer):
        """Set the current user as the board owner on creation."""

        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Delete a board; only the owner is allowed."""

        board = self.get_object()
        if board.owner != request.user:
            raise PermissionDenied(
                'Nur der Eigentümer kann das Board löschen.')
        board.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EmailCheckView(APIView):
    """Look up a user by email address."""

    def get(self, request):
        """Return basic user info for a given email query parameter."""

        email = request.query_params.get('email')
        if not email:
            return Response(
                {'error': 'Email parameter missing.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Email nicht gefunden.'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            UserMiniSerializer(user).data, status=status.HTTP_200_OK
        )
