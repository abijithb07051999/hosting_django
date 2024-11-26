from rest_framework.serializers import ModelSerializer
from . import models

class ExamresultSerializer(ModelSerializer):
    class Meta:
        model = models.ExamresultModel
        fields = '__all__'
        
class OverallExamresultSerializer(ModelSerializer):
    class Meta:
        model = models.OverallExamresultModel
        fields = '__all__'
        
class PassmarkSerializer(ModelSerializer):
    class Meta:
        model = models.PassmarkModel
        fields = '__all__'