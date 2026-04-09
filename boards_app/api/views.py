from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db.models import Q
from django.contrib.auth.models import User
from ..models import Board
from .serializers import BoardSerializer, BoardDetailSerializer, BoardPatchSerializer
from tasks_app.api.serializers import UserMiniSerializer


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardDetailSerializer
        if self.action in ('update', 'partial_update'):
            return BoardPatchSerializer
        return BoardSerializer

    def get_object(self):
        # Erst prüfen ob das Board überhaupt existiert → 404
        try:
            board = Board.objects.get(pk=self.kwargs['pk'])
        except Board.DoesNotExist:
            raise NotFound('Board nicht gefunden.')
        # Dann prüfen ob der User Mitglied oder Owner ist → 403
        user = self.request.user
        if board.owner != user and not board.members.filter(pk=user.pk).exists():
            raise PermissionDenied('Du bist kein Mitglied dieses Boards.')
        return board

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        board = self.get_object()
        if board.owner != request.user:
            raise PermissionDenied(
                'Nur der Eigentümer kann das Board löschen.')
        board.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email parameter missing.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Email nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserMiniSerializer(user).data, status=status.HTTP_200_OK)
