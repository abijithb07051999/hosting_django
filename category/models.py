from django.db import models

class CategoryModel(models.Model):
    category_name = models.TextField()
    category_image = models.TextField()
    