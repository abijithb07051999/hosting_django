from rest_framework.serializers import ModelSerializer
from . import models

class TimetableSerializer(ModelSerializer):
    class Meta:
        model = models.TimetableModel
        fields = '__all__'