# Imports from Django.  # NOQA
from django.conf import settings
from django.core.checks import Error
from django.core.checks import Info
from django.core.checks import register
from django.core.checks import Tags


MISSING_INSTALLED_APP_MSG = """django-assignment-desk requires the app
'{}' to be available and installed.

Please ensure '{}' is in your INSTALLED_APPS list.
"""


MISSING_BOOTSTRAP_MSG = """django-assignment-desk noticed missing
Bootstrap-rendering configuration options.

Your staff pages will render, but some form elements may not be usable
until you add these settings.

Please consult the readme for django-assignment-desk, then add the
recommended configuration under the 'BOOTSTRAP3' name in your settings.
"""


MISSING_RENDERER_MSG = """A required Bootstrap renderer is missing:

>   BOOTSTRAP3['field_renderers']['{}']

Please specify the path to this utility -- it goes in the
'field_renderers' dictionary, which is inside the 'BOOTSTRAP3'
section of your settings file.

Until you do this, some form fields on django-assignment-desk pages may
not render correctly.
"""


@register(Tags.compatibility)
def check_settings(app_configs, **kwargs):
    errors = []

    # Ensure needed helpers are in INSTALLED_APPS.
    required_helper_apps = [
        'django.contrib.humanize',
        'bootstrap3',
        'colorfield',
        'rest_framework'
    ]

    for app_name in required_helper_apps:
        if app_name not in settings.INSTALLED_APPS:
            errors.append(Error(
                MISSING_INSTALLED_APP_MSG.format(app_name, app_name),
                id='assignment_desk.E001'
            ))

    # Ensure django-bootstrap is configured as expected, including the
    # DMN-style "Immaterial" field renderers.
    bootstrap_config = getattr(settings, 'BOOTSTRAP3', None)
    if bootstrap_config and 'field_renderers' in bootstrap_config:
        required_field_renderers = ['default', 'inline', 'immaterial']

        for renderer_key in required_field_renderers:
            if renderer_key not in bootstrap_config['field_renderers']:
                errors.append(Info(
                    MISSING_RENDERER_MSG.format(renderer_key),
                    id='assignment_desk.E002b'
                ))
    else:
        errors.append(Info(
            MISSING_BOOTSTRAP_MSG,
            id='assignment_desk.E002a'
        ))

    return errors
