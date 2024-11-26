from rest_framework.serializers import ModelSerializer
from . import models
class FeesSerializer(ModelSerializer):
    class Meta:
        model = models.FeesModel
        fields = '__all__'
        
class FeesStatusSerializer(ModelSerializer):
    class Meta:
        model = models.FeesStatusModel
        fields = '__all__'