# Imports from python.  # NOQA
from __future__ import unicode_literals


# Imports from Django.
from django.contrib import admin


# Imports from assignment-desk.
from assignment_desk.models import Assignment
from assignment_desk.models import Role
from assignment_desk.models import RoleType
from assignment_desk.models import Week


@admin.register(RoleType)
class RoleTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'priority',),
        }),
        ("Don't touch unlesss you know what you're doing", {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )
    prepopulated_fields = {'slug': ('name',), }


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', ('type', 'priority',),),
        }),
        ('More information', {
            'fields': ('color', 'description',),
        }),
        ("Don't touch unlesss you know what you're doing", {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )
    prepopulated_fields = {'slug': ('name',), }


class AssignmentInline(admin.TabularInline):
    model = Assignment


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    fields = (
        ('beginning_date', 'ending_date',),
        'role_type',
        'extra_information',
    )
    inlines = [AssignmentInline]
