from django import template
from eveapp.models import Follow, OrgNotification, Bookmark, StudentNotification, Event

register = template.Library()


@register.filter(name='is_following')
def is_following(user, organization):
    return Follow.objects.filter(follower=user, organization=organization).exists()

@register.filter
def get_unread_notification_count(user_id):
    ctr = OrgNotification.objects.filter(org_user=user_id, is_read=False).count()
    if ctr > 20:
        count = "20+"
    elif ctr > 0:
        count = str(ctr)
    else:
        count = ""
    return count

@register.filter
def student_get_unread_notification_count(user_id):
    ctr = StudentNotification.objects.filter(student_user=user_id, is_read=False).count()
    if ctr > 20:
        count = "20+"
    elif ctr > 0:
        count = str(ctr)
    else:
        count = ""
    return count


@register.filter(name='has_bookmarked')
def has_bookmarked(user, event):
    return Bookmark.objects.filter(student_user=user, event=event).exists()


@register.filter(name='has_rsvped_going')
def has_rsvped_going(user, event):
    return event.rsvp_yes.filter(user_id=user).exists()


@register.filter(name='has_rsvped_not_going')
def has_rsvped_not_going(user, event):
    return event.rsvp_no.filter(user_id=user).exists()
