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
    path('student_notifications/', StudentNotifView.as_view(), name='student_notifications'),
    path('post_detail/<int:textpost_id>/', PostDetailView.as_view(), name='post_detail'),
    path('n_event_detail/<int:event_id>/', NEventDetailView.as_view(), name='n_event_detail'),
    path('org_notifications/', OrgNotifView.as_view(), name='org_notifications'),
    path('mark_all_as_read/', MarkAllAsRead.as_view(), name='mark_all_as_read'),
    path('mark_one_notif_as_read/<int:notification_id>/', MarkOneAsRead.as_view(), name='mark_one_notif_as_read'),
    path('bookmark_event/<int:event_id>/', BookmarkEventView.as_view(), name='bookmark_event'),
    path('remove_bookmark_event/<int:event_id>/', RemoveBookmarkEventView.as_view(), name='remove_bookmark_event'),
    path('org_announce_list/', OrgAnnouncementsList.as_view(), name='org_announce_list'),
    path('create_text_post/', CreateTextPost.as_view(), name='create_text_post'),
    path('edit_text_post/<int:textpost_id>/', EditTextPost.as_view(), name='edit_text_post'),
    path('student_view_announcements/', StudentViewAnnouncements.as_view(), name='student_view_announcements'),
    path('rsvp_yes/<int:event_id>/',  RSVPYes.as_view(), name='rsvp_yes'),
    path('rsvp_no/<int:event_id>/', RSVPNo.as_view(), name='rsvp_no'),
    path('org_view_rsvps/<int:event_id>/', OrgViewRSVPCount.as_view(), name='org_view_rsvps'),
    path('org_dashboard/', OrgDashboardView.as_view(), name='org_dashboard'),
    path('org_dashboard_followers/', OrgDashboardFollowersView.as_view(), name='org_dashboard_followers'),
    path('student_view_bookmarks/', StudentBookmarksView.as_view(), name='student_view_bookmarks'),
    path('student_view_rsvps/', StudentRSVPSView.as_view(), name='student_view_rsvps'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


