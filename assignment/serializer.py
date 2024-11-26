from rest_framework.serializers import ModelSerializer
from . import models

class AssignmentSerializer(ModelSerializer):
    class Meta:
        model = models.AssignmentModel
        fields = '__all__'