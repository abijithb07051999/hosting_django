from rest_framework.serializers import ModelSerializer
from . import models

class SubjectSerializer(ModelSerializer):
    class Meta:
        model = models.SubjectModel
        fields = '__all__'