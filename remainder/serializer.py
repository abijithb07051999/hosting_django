from rest_framework.serializers import ModelSerializer
from . import models

class RemainderSerializer(ModelSerializer):
    class Meta:
        model = models.RemainderModels
        fields = '__all__'