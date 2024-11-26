from django.urls import path
from . import views
urlpatterns = [
    path('students/', views.StudentView.as_view()),
    path('individual_student/<id>', views.StudentView.as_view()),
]
