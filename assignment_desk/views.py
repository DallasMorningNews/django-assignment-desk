# Imports from python.
import json


# Imports from Django.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView


# Imports from other dependencies.
from editorial_staff.models import Staffer


# Imports from assignment-desk.
from assignment_desk.forms import InlineAssignmentFormset
from assignment_desk.forms import WeekCreationForm
from assignment_desk.forms import WeekEditingForm
from assignment_desk.mixins import InlineFormsetMixin
from assignment_desk.mixins import NavigationContextMixin
from assignment_desk.models import Assignment
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


class WeekListView(LoginRequiredMixin, NavigationContextMixin, ListView):
    queryset = Week.objects.all()
    template_name = 'assignment_desk/weeks/list.html'


class WeekCreateView(LoginRequiredMixin, NavigationContextMixin, CreateView):
    model = Week
    form_class = WeekCreationForm
    template_name = 'assignment_desk/weeks/create_form.html'


class WeekEditView(LoginRequiredMixin, NavigationContextMixin,
                   InlineFormsetMixin, UpdateView):
    model = Week
    template_name = 'assignment_desk/weeks/edit_form.html'

    form_class = WeekEditingForm
    inline_formset_class = InlineAssignmentFormset

    def get_queryset(self):
        return Week.objects.prefetch_related(
            'assignments',
            # 'assignments__staffer',
            'assignments__role',
            'assignments__role__type',
        )

    def get_context_data(self, **kwargs):
        initial_context = super(WeekEditView, self).get_context_data(**kwargs)

        initial_context['role_crosswalk'] = {
            assignment.role.id: {
                'name': assignment.role.name,
                'slug': assignment.role.slug,
            }
            for assignment in self.object.assignments.all()
        }

        raw_staffers = [
            {
                'label': staffer.full_name,
                'value': staffer.email,
                'customProperties': {
                    'id': staffer.id,
                    'firstName': staffer.first_name,
                    'lastName': staffer.last_name,
                    'fullName': staffer.full_name,
                    'formattedName': staffer.render_formatted_name(),
                    'email': staffer.email,
                    'imageURL': staffer.image_url,
                    'active': True,
                },
            } for staffer in Staffer.objects.filter(active=True)
        ]

        initial_context['staffers'] = json.dumps(raw_staffers)

        initial_context['staff_by_id'] = {
            staffer_object['customProperties']['id']: {
                'fullName': staffer_object['customProperties']['fullName'],
                'firstName': staffer_object['customProperties']['firstName'],
                'lastName': staffer_object['customProperties']['lastName'],
                'imageURL': staffer_object['customProperties']['imageURL'],
            } for staffer_object in raw_staffers
        }

        return initial_context

    def get_success_url(self):
        submit_action = self.request.POST.get('submit', '_save')

        if submit_action == '_continue':
            return reverse_lazy(
                'assignment-desk:week-edit',
                kwargs={'pk': self.object.pk}
            )

        return reverse_lazy('assignment-desk:week-list')


class WeekDetailView(LoginRequiredMixin, NavigationContextMixin, DetailView):
    queryset = Week.objects.all().prefetch_related(
        'assignments',
        'assignments__role',
        'assignments__staffer',
    )
    template_name = 'assignment_desk/weeks/detail.html'

    def get_context_data(self, **kwargs):
        context = super(WeekDetailView, self).get_context_data(**kwargs)

        context['role_crosswalk'] = {
            assignment.role.id: {
                'name': assignment.role.name,
                'slug': assignment.role.slug,
            }
            for assignment in self.object.assignments.all()
        }

        return context
