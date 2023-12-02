from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('pricing/', views.pricing, name='pricing'),
    # path('user_signup/', views.user_signup, name='user_signup'),
    path('signup_organization/', RegisterOrg.as_view(), name='signup_organization'),
    path('signup_student/', RegisterStudent.as_view(), name='signup_student'),
    path('login/', LoginView.as_view(), name='login'),

]