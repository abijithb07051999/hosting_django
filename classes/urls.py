from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.ClassesView.as_view()), # TODO: Headers Must Hove School ID
    path('individual_class/<id>', views.ClassesView.as_view())
]
