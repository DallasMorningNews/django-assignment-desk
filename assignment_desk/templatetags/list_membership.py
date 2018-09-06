# Imports from Django.  # NOQA
from django.template.defaulttags import register


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')
