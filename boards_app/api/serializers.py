from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Board
from tasks_app.api.serializers import TaskSerializer, UserMiniSerializer


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for board list and create endpoints."""
    owner_id = serializers.ReadOnlyField(source='owner.id')
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.IntegerField(
        source='tasks.count', read_only=True)
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'member_count', 'ticket_count',
            'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members'
        ]

    def get_member_count(self, obj):
        """Return the number of members in the board."""
        return obj.members.count()

    def get_tasks_to_do_count(self, obj):
        """Return the number of tasks with status 'to-do'."""
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Return the number of high-priority tasks."""
        return obj.tasks.filter(priority='high').count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """Serializer for the board detail endpoint, including members and tasks."""
    owner_id = serializers.ReadOnlyField(source='owner.id')
    members = UserMiniSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardPatchSerializer(serializers.ModelSerializer):
    """Serializer for partial board updates, e.g. updating members."""
    owner_data = UserMiniSerializer(source='owner', read_only=True)
    members_data = UserMiniSerializer(
        source='members', many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members_data', 'members']
