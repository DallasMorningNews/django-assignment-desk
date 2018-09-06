# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


DAY_INTERVAL = None


class AssignmentDeskConfig(AppConfig):
    name = 'assignment_desk'

    def ready(self):
        # Imports from Django.  # NOQA
        from django.conf import settings

        import assignment_desk.checks
        import assignment_desk.signals

        DAY_INTERVAL = getattr(settings, 'ASSIGNMENT_DESK_DAY_INTERVAL', 7)
