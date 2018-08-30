# Imports from Django.  # NOQA
from django.conf import settings
from django.http import HttpResponseRedirect


class NavigationContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(
            NavigationContextMixin,
            self
        ).get_context_data(**kwargs)

        context['navigation_options'] = {
            'logout_url': getattr(
                settings,
                'ASSIGNMENT_DESK_LOGOUT_URL',
                None
            ),
        }

        return context


class InlineFormsetMixin(object):
    form_types = ['form', 'inline_formset']

    def get_form_types(self):
        return self.form_types

    def get_inline_formset_kwargs(self):
        form_kwargs = {'instance': self.object}

        if self.request.method in ('POST', 'PUT',):
            form_kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(InlineFormsetMixin, self).get_context_data(**kwargs)

        # Only add the inline_formset to the context if it doesn't exist
        if 'inline_formset' not in kwargs:
            context['inline_formset'] = self.inline_formset_class(
                **self.get_inline_formset_kwargs()
            )

        # Check the main form and all forms in the inline formset for errors.
        # If any of these forms have a non-zero number of errors, set the
        # 'has_errors' key in the view context to True.

        # This logic exists because django-bootstrap3's built-in formset-error
        # renderer does not properly trace through formsets to display errors.
        if 'has_errors' not in kwargs:
            has_errors = max([
                len([
                    _ for _
                    in context[form_type].errors
                    if len(_) > 0
                ])
                for form_type in self.get_form_types()
            ]) > 0

            context.update(
                dict(
                    has_errors=has_errors
                )
            )

        return context

    def form_valid(self, form):
        """Override the form validator to handle"""
        context = self.get_context_data()
        inline_formset = context['inline_formset']

        if inline_formset.is_valid() and form.is_valid():
            # Save the ModelForm object, then move on to the inline formset
            self.object = form.save()
            inline_formset.instance = self.object

            # If the inline supports ordering and our view specifies an order
            # field, store the order on the model
            if inline_formset.can_order and hasattr(self, 'order_field'):
                order_field = getattr(self, 'order_field')
                for form in inline_formset.ordered_forms:
                    setattr(
                        form.instance,
                        order_field,
                        form.cleaned_data['ORDER']
                    )

            inline_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(
                form=form,
                inline_formset=inline_formset
            ))
