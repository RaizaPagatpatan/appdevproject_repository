from django import template
from eveapp.models import Follow

register = template.Library()


@register.filter(name='is_following')
def is_following(user, organization):
    return Follow.objects.filter(follower=user, organization=organization).exists()