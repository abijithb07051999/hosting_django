from rest_framework.serializers import ModelSerializer
from . import models

class ClassesSerializer(ModelSerializer):
    class Meta:
        model = models.ClassesModel
        fields = '__all__'