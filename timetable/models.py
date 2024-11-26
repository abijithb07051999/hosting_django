from django.db import models
from subject.models import SubjectModel
from classes.models import ClassesModel

class TimetableModel(models.Model):
    subject_id = models.ForeignKey(SubjectModel, on_delete=models.CASCADE,null=True)
    subject_name=models.TextField(null=True)
    class_id = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    weekday = models.TextField()
    start_time = models.TextField()
    end_time = models.TextField()
