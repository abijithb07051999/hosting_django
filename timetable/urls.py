from django.urls import path
from . import views
urlpatterns = [
    path('timetables/', views.TimetableView.as_view()), # TODO: Headers Must Have Class ID
    path('individual_timetable/<id>', views.TimetableView.as_view()),
]
