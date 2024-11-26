from django.urls import path
from . import views

urlpatterns = [
    path('attendances/', views.AttendaceView.as_view()), # TODO: Headers Must Have Student ID and Class ID
    path('individual_attendance/<id>', views.AttendaceView.as_view()),
    path('allstudentsattendance/',views.AllStudentsAttendanceView.as_view()), # TODO: Headers Must Have Class ID
    path('attendance_by_date/',views.AttendanceByDate.as_view()), # TODO: Headers must have Class ID
]