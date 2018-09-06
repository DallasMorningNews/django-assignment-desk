# Imports from Django.  # NOQA
from django.conf import settings

__version__ = (0, 1, 7)

default_app_config = 'assignment_desk.apps.AssignmentDeskConfig'  # NOQA


DAY_INTERVAL = getattr(settings, 'ASSIGNMENT_DESK_DAY_INTERVAL', 7)
