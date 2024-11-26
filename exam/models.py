from django.db import models
from classes.models import ClassesModel
from subject.models import SubjectModel

class ExamModel(models.Model):
    exam_class_id = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    exam_name = models.TextField()
    exam_start_date = models.TextField()
    exam_end_date = models.TextField()

class ExamTimetableModel(models.Model):
    exam_id = models.ForeignKey(ExamModel, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(SubjectModel, on_delete=models.CASCADE)
    start_time = models.TextField()
    end_time = models.TextField()
    portions = models.TextField()
    exam_date = models.TextField()
    