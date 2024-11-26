"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('category/',include('category.urls')),
    path('school/',include('school.urls')),
    path('teacher/',include('teacher.urls')),
    path('class/',include('classes.urls')),
    path('holiday/',include('holiday.urls')),
    path('student/',include('student.urls')),
    path('fees/',include('fees.urls')),
    path('attendance/',include('attendance.urls')),
    path('remainder/',include('remainder.urls')),
    path('subject/',include('subject.urls')),
    path('timetable/',include('timetable.urls')),
    path('portion/',include('portion.urls')),
    path('assignment/',include('assignment.urls')),
    path('exam/',include('exam.urls')),
    path('examresult/',include('examresult.urls')),
    path('parent/', include('parent.urls')),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)+static(settings.PLACEHOLDER, document_root=settings.PLACEHOLDER_ROOT)
