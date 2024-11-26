from django.db import models
from category.models import CategoryModel

class SchoolModel(models.Model):
    school_name = models.TextField()
    school_image = models.TextField()
    school_passkey = models.TextField()
    school_address = models.TextField(null=True)
    contact_1 = models.BigIntegerField(null=True)
    contact_2 = models.BigIntegerField(null=True)
    subscription_month = models.IntegerField(null=True)
    amount_per_student = models.IntegerField(null=True)
    school_enabled = models.BooleanField(default=True)
    
class RolesModel(models.Model):
    school_id = models.ForeignKey(SchoolModel, on_delete=models.CASCADE, null=False)
    role_name = models.TextField()
    role_username = models.TextField()
    role_password = models.TextField()
    
# class PermissionModel(models.Model):
#     category_id = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=False)
#     role_id = models.ForeignKey(RolesModel, on_delete=models.CASCADE, null=False)
#     view = models.BooleanField(null=False, default=False)