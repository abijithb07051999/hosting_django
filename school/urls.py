from django.urls import path
from . import views
urlpatterns = [
    path('schools/', views.SchoolView.as_view()),
    path('school_enable/<id>', views.SchoolEnableDisable.as_view()),
    path('individual_school/<id>', views.SchoolView.as_view()),
    path('roles/', views.RoleView.as_view()),
    path('individual_role/<id>', views.RoleView.as_view()),
          
    path('schoollogin/', views.SchoolLoginView.as_view()),
    path('login/', views.LoginView.as_view()),# TODO: Headers Must Have School ID
    # path('get_category/', views.CategorySchool.as_view()), # TODO: Headers Must Have Role ID
    # path('permissions/', views.PermissionView.as_view()),
    # path('individual_permission/<id>', views.PermissionView.as_view()),
]
