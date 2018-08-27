# Imports from Django.
from django import forms


# Imports from other dependencies.
from editorial_staff.models import Staffer


# Imports from assignment-desk.
from assignment_desk.models import Assignment
from assignment_desk.models import Week


EXTRA_INFORMATION_HELP_TEXT = """
<strong>Optional.</strong> Use this field if you want to include a note
(with extra explanations, descriptions, etc.) that will be displayed
alongside this assignment list.
"""


class WeekCreationForm(forms.ModelForm):
    class Meta:
        model = Week

        fields = ['beginning_date', 'role_type', 'extra_information']
        labels = {'role_type': 'Type',}
        help_texts = {
            'extra_information': EXTRA_INFORMATION_HELP_TEXT,
        }


class WeekEditingForm(forms.ModelForm):
    class Meta:
        model = Week

        fields = ['extra_information']
        help_texts = {
            'extra_information': EXTRA_INFORMATION_HELP_TEXT,
        }


class AssignmentForm(forms.ModelForm):
    # staffer = forms.CharField(widget=forms.HiddenInput())
    staffer = forms.ModelChoiceField(
        queryset=Staffer.objects.all(),
        required=False,
        widget=forms.TextInput
    )

    class Meta:
        model = Assignment
        fields = [
            'staffer',
            'notes',
        ]

InlineAssignmentFormset = forms.inlineformset_factory(
    Week,
    Assignment,
    form=AssignmentForm,
    extra=0,
    can_delete=False,
)
