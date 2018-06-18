# Imports from Django.  # NOQA
from django.conf.urls import include
from django.conf.urls import url


# Imports from assignment-desk.
from assignment_desk.views import index_view
from assignment_desk.views import WeekCreateView
from assignment_desk.views import WeekDetailView
from assignment_desk.views import WeekEditView
from assignment_desk.views import WeekListView


app_name = 'assignment-desk'


urlpatterns = [
    url('^$', index_view, name='index'),
    url('^weeks/', include([
        url('^$', WeekListView.as_view(),
            name='week-list'),
        url('^create/$', WeekCreateView.as_view(),
            name='week-create'),
        url('^(?P<pk>[0-9]+)/', include([
            url('^$', WeekDetailView.as_view(),
                name='week-detail'),
            url('^edit/$', WeekEditView.as_view(),
                name='week-edit'),
            # url('^delete/$', WeekDeleteView.as_view(),
            #     name='week-delete'),
        ])),
    ])),
]
