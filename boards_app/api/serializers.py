# boards_app/api/serializers.py
from rest_framework import serializers
from ..models import Board
from tasks_app.api.serializers import TaskSerializer
# da deer Boardserializer von ModelsSerializer erbt, müssen wir nicht mehr alle Felder manuell definieren, sondern können sie automatisch generieren lassen.


class BoardSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    ticket_count = serializers.IntegerField(
        source='tasks.count', read_only=True)
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'members', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'tasks']

    def get_tasks_to_do_count(self, obj):
        # Greift auf die Related Name 'tasks' aus deinem Model zu
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()


# from rest_framework import serializers
# from ..models import Board


# class BoardSerializer(serializers.ModelSerializer):

    # class Meta:
        # model = Board
        # fields = ["id", "title", "owner", "members"]

    # def create(self, validated_data):
        # Beim Erstellen eines Boards wird der Owner automatisch gesetzt
        # owner = self.context['request'].user
        # board = Board.objects.create(owner=owner, **validated_data)
       # return board
