from django.urls import path
from . import views
urlpatterns = [
    path('subjects/', views.SubjectView.as_view()), # TODO: Headers Must Have Class ID
    path('individual_subject/<id>', views.SubjectView.as_view()) # TODO: Headers Must Have Class ID
    
]
