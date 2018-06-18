# Imports from Django.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView


# Imports from assignment-desk.
from assignment_desk.models import Role
from assignment_desk.models import Week


DAYS_IN_WEEK = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',
]


def index_view(request):
    return HttpResponse('Hello, world. You\'re at the assignment-desk index.')


class WeekListView(LoginRequiredMixin, ListView):
    queryset = Week.objects.all()
    template_name = 'assignment_desk/weeks/list.html'


class WeekCreateView(LoginRequiredMixin, CreateView):
    model = Week
    fields = ['beginning_date', 'role_type', 'extra_information']
    template_name = 'assignment_desk/weeks/create_form.html'


class WeekEditView(LoginRequiredMixin, UpdateView):
    model = Week
    fields = ['extra_information']
    template_name = 'assignment_desk/weeks/edit_form.html'


class WeekDetailView(LoginRequiredMixin, DetailView):
    queryset = Week.objects.all().prefetch_related(
        'assignments',
        'assignments__role',
        'assignments__staffer',
    )
    template_name = 'assignment_desk/weeks/detail.html'

    def get_context_data(self, **kwargs):
        context = super(WeekDetailView, self).get_context_data(**kwargs)

        grouped_assignments = {}

        for assignment in self.object.assignments.all():
            if assignment.role.name not in grouped_assignments:
                grouped_assignments[assignment.role.name] = {}

            day_name = assignment.day.strftime('%A').lower()

            grouped_assignments[
                assignment.role.name
            ][day_name] = assignment.staffer

        roles_for_type = Role.objects.filter(
            type_id=self.object.role_type.pk
        ).order_by('priority')

        context['available_roles'] = roles_for_type

        context['roles_with_assignments'] = {
            role.slug: {
                (day): (
                    grouped_assignments[role.name][day]
                    if role.name in grouped_assignments
                    and day in grouped_assignments[role.name]
                    else None
                ) for day in DAYS_IN_WEEK
            }
            for role in roles_for_type
        }

        # print(context['roles_with_assignments']['230-meeting']['friday'].name)

        return context
