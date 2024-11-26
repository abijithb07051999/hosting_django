from django.urls import path
from . import views
urlpatterns = [
    path('fees/', views.FeesView.as_view()),   # TODO: Headers Must Have Class ID
    path('individual_fee/<id>', views.FeesView.as_view()),
    path('feesStatus/', views.FeesStatusView.as_view()), # TODO: Headers Must Have Class Id and Fees ID
    path('individual_fee_status/<id>', views.FeesStatusView.as_view()), 
]
