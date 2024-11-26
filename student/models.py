from django.db import models
from classes.models import ClassesModel
from school.models import SchoolModel

class StudentModel(models.Model):
    student_unique_id = models.TextField()
    student_name = models.TextField()
    student_date_of_birth = models.TextField()
    student_image = models.TextField(null=True)
    student_gender = models.TextField()
    student_address = models.TextField()
    student_blood_group = models.TextField()
    guardian_1_name = models.TextField(null=True)
    guardian_1_image = models.TextField(null=True)
    guardian_1_relation = models.TextField(null=True)
    guardian_1_contact_1 = models.BigIntegerField()
    guardian_1_contact_2 = models.BigIntegerField(null=True)
    guardian_2_name = models.TextField(null=True,)
    guardian_2_image = models.TextField(null=True,)
    guardian_2_relation = models.TextField(null=True)
    guardian_2_contact_1 = models.BigIntegerField(null=True)
    guardian_2_contact_2 = models.BigIntegerField(null=True)
    student_class_id = models.ForeignKey(ClassesModel, on_delete=models.CASCADE, null=False)
    student_school_id = models.ForeignKey(SchoolModel, on_delete=models.CASCADE, null=False)
    

    