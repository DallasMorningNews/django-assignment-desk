# Imports from Django.  # NOQA
from django.forms import CheckboxInput
# from django.forms import CheckboxSelectMultiple
# from django.forms import ClearableFileInput
from django.forms import DateInput
from django.forms import EmailInput
# from django.forms import FileInput
# from django.forms import MultiWidget
from django.forms import NumberInput
# from django.forms import RadioSelect
from django.forms import Select
from django.forms import Textarea
from django.forms import TextInput
from django.forms import URLInput


# Imports from other dependencies.
from bootstrap3.forms import render_label
from bootstrap3.renderers import FieldRenderer
from bootstrap3.text import text_value
from bootstrap3.utils import add_css_class


WIDGETS_WITH_UNDERLINE = (
    TextInput,
    DateInput,
    NumberInput,
    EmailInput,
    URLInput,
    Textarea,
)

WIDGETS_AFTER_LABEL = (
    Select,
)


class ImmaterialFieldRenderer(FieldRenderer):
    def post_widget_render(self, html):
        """Override adds helper class to checkboxes."""
        if isinstance(self.widget, CheckboxInput):
            return self.put_inside_label(
                '{}{}'.format(
                    html,
                    '<span class="ripple"></span><i class="helper"></i>'
                )
            )
        else:
            return super(ImmaterialFieldRenderer, self).post_widget_render(
                html
            )

    def add_label(self, html):
        """Override adds label _after_ input, & sometimes bar class."""
        label = self.get_label()
        if label:
            if isinstance(self.widget, WIDGETS_WITH_UNDERLINE):
                html = '{}{}{}'.format(
                    html,
                    render_label(
                        label,
                        label_for=self.field.id_for_label,
                        label_class=self.get_label_class()
                    ),
                    '<i class="bar"></i>'
                )
            elif isinstance(self.widget, WIDGETS_AFTER_LABEL):
                html = '{}{}'.format(
                    html,
                    render_label(
                        label,
                        label_for=self.field.id_for_label,
                        label_class=self.get_label_class()
                    )
                )
            elif isinstance(self.widget, Textarea):
                html = '{}{}'.format(
                    html,
                    render_label(
                        label,
                        label_for=self.field.id_for_label,
                        label_class=self.get_label_class()
                    )
                )
            else:
                html = '{}{}'.format(
                    render_label(
                        label,
                        label_for=self.field.id_for_label,
                        label_class=self.get_label_class()
                    ),
                    html
                )
        return html

    def get_form_group_class(self):
        """Override adds 'group_<field_name>' class to each group."""
        form_group_class = super(
            ImmaterialFieldRenderer,
            self
        ).get_form_group_class()

        named_group_class = 'group_{}'.format(self.field.name)

        form_group_class = add_css_class(form_group_class, named_group_class)

        return form_group_class

    def _render(self):
        """Overrides for root renderer.

        Adds helptext (append_to_field) later than usual, and adds class
        'select' when rendering a select box.
        """
        # See if we're not excluded
        if self.field.name in self.exclude.replace(' ', '').split(','):
            return ''
        # Hidden input requires no special treatment
        if self.field.is_hidden:
            return text_value(self.field)

        # Render the widget
        self.add_widget_attrs()
        if (isinstance(self.widget, Select)):
            new_classes = add_css_class(self.widget.attrs['class'], 'select')
            self.widget.attrs['class'] = new_classes

        if isinstance(self.widget, Textarea):
            self.widget.attrs['autocomplete'] = 'nope'
            # self.widget.attrs['autocorrect'] = 'off'
            # self.widget.attrs['autocapitalize'] = 'off'
            # self.widget.attrs['spellcheck'] = 'false'

            self.widget.attrs['rows'] = 6

        html = self.field.as_widget(attrs=self.widget.attrs)

        self.restore_widget_attrs()

        # Start post render
        html = self.post_widget_render(html)

        html = self.wrap_widget(html)

        html = self.make_input_group(html)

        html = self.wrap_field(html)
        html = self.add_label(html)
        html = self.append_to_field(html)
        html = self.wrap_label_and_field(html)
        return html
