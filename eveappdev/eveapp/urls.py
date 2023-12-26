from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.Home.as_view(), name="home_view"),
    path('services/', Services.as_view(), name="services"),
    path('pricing/', views.pricing, name='pricing'),
    path('pricing_org/', views.pricing_org, name='pricing_org'),
    # path('user_signup/', views.user_signup, name='user_signup'),
    path('signup_organization/', RegisterOrg.as_view(), name="signup_organization"),
    path('signup_student/', RegisterStudent.as_view(), name="signup_student"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name='logout'),
    path('student_home/', ShowStudentHome.as_view(), name="student_home"),
    path('org_home/', OrgHome.as_view(), name="org_home"),
    # path('edit_profile/', EditProfile.as_view(), name="edit_profile"),
    path('update_profile/', UpdateProfile.as_view(), name="update_profile"),
    path('verify/', Verify.as_view(), name="verify"),
    path('verify_home/', OrgVerifyView.as_view(), name="verify_home"),
    path('org_list/', OrgList.as_view(), name="org_list"),
    path('org_event_list/', OrgEventListView.as_view(), name="org_event_list"),
    path('student_event_view/', EventStudentView.as_view(), name="student_event_view"),
    path('add_event/', AddEvent.as_view(), name="add_event"),
    path('edit_event/<int:event_id>/', EditEvent.as_view(), name='edit_event'),
    path('org_profile/<int:org_id>/', ProfileView.as_view(), name='org_profile'),
    path('follow_organization/<int:org_id>/', FollowOrganizationView.as_view(), name='follow_organization'),
    path('unfollow_organization/<int:org_id>/', UnfollowOrganizationView.as_view(), name='unfollow_organization'),
    path('follow_org_listview/<int:org_id>/', FollowOrgListView.as_view(), name='follow_org_listview'),
    path('unfollow_org_listview/<int:org_id>/', UnfollowOrgListView.as_view(), name='unfollow_org_listview'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


