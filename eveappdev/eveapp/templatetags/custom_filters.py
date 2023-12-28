from django import template
from eveapp.models import Follow, OrgNotification

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