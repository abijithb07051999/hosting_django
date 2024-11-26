from django.urls import path
from . import views

urlpatterns = [
    path('holidaies/', views.HolidyView.as_view()),
    path('individual_holiday/<id>', views.HolidyView.as_view()),
]
