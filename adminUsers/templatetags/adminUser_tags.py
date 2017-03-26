import datetime

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe, SafeData, mark_for_escaping

from adminUsers.models import AdminUser

register = template.Library()



@register.filter
def isAdminUser(value):
    if AdminUser.objects.filter(email=value):
        return True
    else:
        return False



