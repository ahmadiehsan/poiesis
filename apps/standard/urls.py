from django.urls import path

from .views import (
    SelectStandardView,
    NamingReactView,
    NamingDjangoView,
    RulesReactView,
    RulesDjangoView,
    RulesPOView,
    TaskPOView,
)

app_name = 'standard'

urlpatterns = [
    path('', SelectStandardView.as_view(), name='select-standard'),

    path('naming/react/', NamingReactView.as_view(), name='naming-react'),
    path('naming/django/', NamingDjangoView.as_view(), name='naming-django'),

    path('rules/react/', RulesReactView.as_view(), name='rules-react'),
    path('rules/django/', RulesDjangoView.as_view(), name='rules-django'),
    path('rules/po/', RulesPOView.as_view(), name='rules-po'),

    path('task/po/', TaskPOView.as_view(), name='task-po'),
]
