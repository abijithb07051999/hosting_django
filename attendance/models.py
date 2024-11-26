from django.db import models
from classes.models import ClassesModel
from student.models import StudentModel

class AttendanceModel(models.Model):
    class_id = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    date = models.TextField()
    weekday = models.TextField()
    student_id = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    month = models.TextField()
    attendance_status = models.BooleanField(default=False)