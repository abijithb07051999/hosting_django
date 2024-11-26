from rest_framework.serializers import ModelSerializer
from . import models

class HolidaySerializer(ModelSerializer):
    class Meta:
        model = models.HolidayModel
        fields = '__all__'