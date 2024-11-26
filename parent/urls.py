from django.urls import path
from . import views
urlpatterns = [
    # login
    path('login/', views.LoginView.as_view()),# TODO: Headers Must Have School ID 
    # profile
    path('profile/', views.ProfileView.as_view()), # TODO: Headers Must Have School ID and Student ID
    # report_card
    path('report_card/', views.ReportCardView.as_view()),# TODO: Headers Must Have School ID and Student ID
    # time_table
    path('time_table/', views.TimeTableView.as_view()),# TODO: Headers Must Have School ID and Class ID
    # exam_time_table
    path('exam_time_table/', views.ExamTimeTableView.as_view()),# TODO: Headers Must Have School ID and Class ID
    # faculties
    path('faculties/', views.FacultiesView.as_view()),# TODO: Headers Must Have School ID and Class ID
    # fees
    path('fees/', views.FeesView.as_view()),# TODO: Headers Must Have School ID , Student ID and Class ID
    # attendance
    path('attendance/', views.AttendanceView.as_view()),# TODO: Headers Must Have School ID and Student ID
    # remainder
    path('remainder/', views.RemainderView.as_view()),# TODO: Headers Must Have School ID and Class ID
    # portion
    path('portion/', views.PortionView.as_view()),# TODO: Headers Must Have School ID and Class ID
    # assignment
    path('assignment/', views.AssignmentView.as_view()),# TODO: Headers Must Have School ID and Class ID
]
