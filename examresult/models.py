from django.db import models
from student.models import StudentModel
from exam.models import ExamModel, ExamTimetableModel
from school.models import SchoolModel

class ExamresultModel(models.Model):
    student_id = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(ExamModel, on_delete=models.CASCADE)
    exam_time_table = models.ForeignKey(ExamTimetableModel, on_delete=models.CASCADE)
    mark = models.IntegerField()
    grade = models.TextField()
    
class OverallExamresultModel(models.Model):
    student_id = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(ExamModel, on_delete=models.CASCADE)
    exam_total = models.IntegerField()
    exam_grade = models.TextField()
    
class PassmarkModel(models.Model):
    school_id = models.ForeignKey(SchoolModel, on_delete=models.CASCADE)
    passmark = models.IntegerField()