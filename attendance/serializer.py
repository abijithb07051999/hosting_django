from rest_framework.serializers import ModelSerializer
from . import models

class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = models.AttendanceModel
        fields = '__all__'