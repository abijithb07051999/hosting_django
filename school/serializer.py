from rest_framework.serializers import ModelSerializer
from . import models

class SchoolSerializer(ModelSerializer):
    class Meta:
        model = models.SchoolModel
        fields = '__all__'
        
class RoleSerializer(ModelSerializer):
    class Meta:
        model = models.RolesModel
        fields = '__all__'
        
# class PermissionSerializer(ModelSerializer):
#     class Meta:
#         model = models.PermissionModel
#         fields = '__all__'