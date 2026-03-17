from django.db import models
from django.conf import settings


class Board(models.Model):
    title = models.CharField(max_length=255)
    # Der Ersteller des Boards
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_boards"
    )
    # Die Teilnehmer (für board.js: currentBoard.members)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="boards"
    )

    def __str__(self):
        return self.title
