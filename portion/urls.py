from django.urls import path
from . import views
urlpatterns = [
    path('portions/', views.PortionView.as_view()),
    path('individual_portion/<id>', views.PortionView.as_view()),
]
