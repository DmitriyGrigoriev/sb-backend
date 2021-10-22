from rest_framework import serializers


### Template serializer
class TemplateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    version = serializers.IntegerField(default=0)
    class Meta:
        abstract = True
        fields = (
            'id','version',
        )
