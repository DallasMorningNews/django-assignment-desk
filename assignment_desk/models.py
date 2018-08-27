# Imports from python.  # NOQA
from __future__ import unicode_literals

# Imports from Django.
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.dateformat import format as df


# Imports from other dependencies.
from colorfield.fields import ColorField
from editorial_staff.models import Staffer


# Imports from assignment-desk.
from assignment_desk.utils import get_latest_monday
from assignment_desk.utils import get_next_sunday


class RoleType(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    priority = models.PositiveSmallIntegerField(default=10)

    class Meta:  # NOQA
        ordering = ['priority', 'name']

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    color = ColorField(default='#0185D3')

    type = models.ForeignKey(RoleType, related_name='roles')

    priority = models.PositiveSmallIntegerField(default=10)

    class Meta:  # NOQA
        ordering = ['priority', 'name']

    def __str__(self):
        return '{} ({})'.format(self.name, self.type.name)


class Week(models.Model):
    beginning_date = models.DateField(default=get_latest_monday)
    ending_date = models.DateField(default=get_next_sunday)

    role_type = models.ForeignKey(
        RoleType,
        related_name='weeks',
        blank=True,
        null=True
    )

    assigned_staffers = models.ManyToManyField(
        Staffer,
        through='Assignment'
    )

    extra_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Week of {}'.format(df(self.beginning_date, 'N j, Y'))


class Assignment(models.Model):
    week = models.ForeignKey(
        Week,
        related_name='assignments',
        on_delete=models.CASCADE
    )
    staffer = models.ForeignKey(
        Staffer,
        related_name='assignments',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    role = models.ForeignKey(
        Role,
        related_name='assignments',
        on_delete=models.CASCADE
    )
    day = models.DateField()
    notes = models.TextField(blank=True, null=True)

    class Meta:  # NOQA
        ordering = ['role', 'day']

    def __str__(self):
        return '{} — {} for {} ({})'.format(
            self.staffer,
            self.role.name,
            self.role.type.name,
            df(self.day, 'N j, Y')
        )
