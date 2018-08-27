# Imports from python.
from datetime import timedelta


# Imports from Django.
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver


# Imports from assignment-desk.
from assignment_desk.models import Assignment
from assignment_desk.models import Week


@receiver(post_save, sender=Week, dispatch_uid="populate_assignments")
def create_assignments_for_empty_week(sender, instance, **kwargs):
    if instance.assignments.count() == 0 and instance.role_type:
        roles_to_add = []

        for role in instance.role_type.roles.all():
            roles_to_add.extend([
                Assignment(
                    week_id=instance.id,
                    role_id=role.id,
                    day=(instance.beginning_date + timedelta(days=day_delta))
                ) for day_delta in range(7)
            ])

        with transaction.atomic():
            Assignment.objects.bulk_create(roles_to_add)
