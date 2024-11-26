from django.db import models
from classes.models import ClassesModel
from teacher.models import TeacherModel

class SubjectModel(models.Model):
    subject_name = models.TextField()
    subject_class_id = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    subject_teacher_id = models.ForeignKey(TeacherModel, on_delete=models.CASCADE)