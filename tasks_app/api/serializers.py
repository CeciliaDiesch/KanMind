from rest_framework import serializers
from django.utils import timezone
from ..models import Task


class TaskSerializer(serializers.ModelSerializer):
    # Ein berechnetes Feld für das Frontend (Dashboard-Anforderung)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date',
                  'status', 'priority', 'is_overdue']

    def validate_due_date(self, value):
        """
        Spezifische Validierung für das Feld due_date.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "Das Datum darf nicht in der Vergangenheit liegen!")
        return value

    def get_is_overdue(self, obj):
        return obj.due_date < timezone.now().date() and obj.status != 'done'
