from django.db import models
from school.models import SchoolModel
from teacher.models import TeacherModel

class ClassesModel(models.Model):
    class_name = models.TextField()
    class_number = models.IntegerField()
    class_section = models.TextField(null=True)
    school_id = models.ForeignKey(SchoolModel, on_delete=models.CASCADE, null=False)
    teacher_id = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, null=False)
    