# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class AssignmentDeskConfig(AppConfig):
    name = 'assignment_desk'

    def ready(self):
        import assignment_desk.signals
