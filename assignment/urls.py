from django.urls import path
from . import views
urlpatterns = [
    path('assignments/', views.AssignmentView.as_view()),
    path('individual_assignment/<id>', views.AssignmentView.as_view()),
]
