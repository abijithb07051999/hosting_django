from rest_framework.serializers import ModelSerializer
from . import models

class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.CategoryModel
        fields = '__all__'