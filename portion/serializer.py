from rest_framework.serializers import ModelSerializer
from . import models

class PortionSerializer(ModelSerializer):
    class Meta:
        model = models.PortionModel
        fields = '__all__'