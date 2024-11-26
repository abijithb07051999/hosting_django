from django.db import models
from school.models import SchoolModel

class HolidayModel(models.Model):
    date = models.TextField()
    weekday = models.TextField()
    reason = models.TextField()
    school_id = models.ForeignKey(SchoolModel, on_delete=models.CASCADE, null=False)
    
    