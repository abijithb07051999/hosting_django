from django.urls import path
from . import views
urlpatterns = [
    path('categories/', views.CategoryView.as_view()),
    path('individual_category/<id>', views.CategoryView.as_view()),
]