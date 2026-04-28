from rest_framework.exceptions import PermissionDenied


def check_board_member(user, board):
    """Raise PermissionDenied if user is not owner or member of the board."""

    if board.owner != user and not board.members.filter(pk=user.pk).exists():
        raise PermissionDenied('Du bist kein Mitglied dieses Boards.')
