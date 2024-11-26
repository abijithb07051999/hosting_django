from django.db import models
from school.models import SchoolModel

class TeacherModel(models.Model):
    teacher_name = models.TextField()
    teacher_image = models.TextField()
    teacher_date_of_birth = models.TextField()
    teacher_gender = models.TextField()
    teacher_blood_group = models.TextField()
    teacher_address = models.TextField()
    teacher_contact_1 = models.BigIntegerField()
    teacher_contact_2 = models.BigIntegerField(null=True)
    teacher_school_id = models.ForeignKey(SchoolModel, on_delete=models.CASCADE, null=False)
    
    
    
    
    