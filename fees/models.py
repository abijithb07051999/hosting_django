from django.db import models
from classes.models import ClassesModel
from student.models import StudentModel

class FeesModel(models.Model):
    fees_amount = models.IntegerField()
    fees_last_date = models.TextField()
    fees_reason = models.TextField()
    fees_class_id = models.ForeignKey(ClassesModel, on_delete=models.CASCADE, null=False)
    
class FeesStatusModel(models.Model):
    fees_id = models.ForeignKey(FeesModel, on_delete=models.CASCADE, null=False)
    fees_class_id = models.ForeignKey(ClassesModel, on_delete=models.CASCADE, null=False)
    fees_student_id = models.ForeignKey(StudentModel, on_delete=models.CASCADE, null=False)
    fees_paid_date = models.TextField()
    paid_status = models.BooleanField(default=False)
