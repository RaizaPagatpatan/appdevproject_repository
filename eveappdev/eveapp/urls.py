from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('pricing/', views.pricing, name='pricing'),
    # path('user_signup/', views.user_signup, name='user_signup'),
    path('signup_organization/', RegisterOrg.as_view(), name="signup_organization"),
    path('signup_student/', RegisterStudent.as_view(), name="signup_student"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name='logout'),
    path('student_home/', ShowStudentHome.as_view(), name="student_home"),
    path('org_home/', OrgHome.as_view(), name="org_home"),
    path('verify/', Verify.as_view(), name="verify"),
    path('verify_home/', OrgVerifyView.as_view(), name="verify_home"),
    path('org_list/', OrgList.as_view(), name="org_list"),
    path('org_event_list/', OrgEventListView.as_view(), name="org_event_list"),
    path('student_event_view/', EventStudentView.as_view(), name="student_event_view"),
    path('add_event/', AddEvent.as_view(), name="add_event"),

]
