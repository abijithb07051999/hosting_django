from django.urls import path
from . import views

urlpatterns = [
    path('remainders/', views.RemainderView.as_view()), #  TODO: Headers Must Have Class ID
    path('individual_remainder/<id>', views.RemainderView.as_view()),
]
 