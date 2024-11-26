from django.urls import path
from . import views
urlpatterns = [
#  path('examresults/', views.ExamresultView.as_view()),   # TODO: Headers Must Have Exam ID
#  path('individual_examresult/<id>', views.ExamresultView.as_view()),   
#  path('overallexamresults/', views.OverallExamresultView.as_view()),   # TODO: Headers Must Have Exam ID
#  path('individual_overallexamresult/<id>', views.OverallExamresultView.as_view()),   
 path('passmarks/', views.PassmarkView.as_view()),   # TODO: Headers Must Have School ID
 path('individual_passmark/<id>', views.PassmarkView.as_view()), 
 
 path('studentexamresult/',views.ExamResultForStudentView.as_view()),  # TODO: Headers Must Have Class ID
 path('addexamresult/',views.AddStudentExamResult.as_view()),   # TODO: Headers Must Have Student ID
 
]
