from django.urls import path
from . import views
urlpatterns = [
    path('teachers/', views.TeacherView.as_view()), # TODO: Headers Must Have School ID
    path('teachers/<id>', views.TeacherView.as_view()),
    path('individual_teacher/<id>', views.TeacherView.as_view()),
]
