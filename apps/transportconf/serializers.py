from rest_framework.serializers import ModelSerializer

from .models import Terminal

class TerminalSerializer(ModelSerializer):
    class Meta:
        model = Terminal
        fields = ['id','name',]