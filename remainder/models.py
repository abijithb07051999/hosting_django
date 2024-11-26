from django.db import models
from classes.models import ClassesModel

class RemainderModels(models.Model):
    class_id = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    date = models.TextField()
    weekday = models.TextField()
    remainder = models.TextField()

