from django.urls import path
from . import views
urlpatterns = [
    path('exams/', views.ExamView.as_view()), # TODO: Headers Must Have Class ID
    # path('individual_exam/<id>', views.ExamView.as_view()),
    path('examtimetables/', views.ExamTimetableView.as_view()), # ? To Add Data // 1) Individual Exam Details GET (Headers MUST Have Exam ID // Add New Exam (POST) 
    # path('individual_examtimetable/<id>', views.ExamTimetableView.as_view()), # 
    path('classexams/',views.Class_based_ExamTimeTable.as_view()), # TODO: Headers Must Have Class ID and School ID (To Get Data) // GET
    path('individualclassexams/<id>',views.Class_based_ExamTimeTable.as_view()), # TODO : PUT and DELETE
]