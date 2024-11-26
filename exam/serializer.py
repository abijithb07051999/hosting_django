from rest_framework.serializers import ModelSerializer
from . import models

class ExamSerializer(ModelSerializer):
    class Meta:
        model = models.ExamModel
        fields = '__all__'
        
class ExamTimetableSerializer(ModelSerializer):
    class Meta:
        model = models.ExamTimetableModel
        fields = '__all__'