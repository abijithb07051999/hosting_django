from django.db import models
from classes.models import ClassesModel
from subject.models import SubjectModel

class AssignmentModel(models.Model):
    class_id = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(SubjectModel, on_delete=models.CASCADE)
    date = models.TextField()
    weekday = models.TextField()
    assignment = models.TextField()
