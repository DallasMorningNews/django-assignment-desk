# Imports from python.  # NOQA
import datetime


# Imports from Django.
from django.template.defaulttags import register


@register.filter
def add_days(original_value, num_days):
   return original_value + datetime.timedelta(days=num_days)
