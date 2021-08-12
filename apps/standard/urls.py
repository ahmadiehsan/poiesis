from django.urls import path

from .views import (
    SelectFrameworkView,
    NamingReactView,
    NamingDjangoView,
    RulesReactView,
    RulesDjangoView
)

app_name = 'standard'

urlpatterns = [
    path('', SelectFrameworkView.as_view(), name='select-framework'),
    path('naming/react/', NamingReactView.as_view(), name='naming-react'),
    path('naming/django/', NamingDjangoView.as_view(), name='naming-django'),
    path('rules/react/', RulesReactView.as_view(), name='rules-react'),
    path('rules/django/', RulesDjangoView.as_view(), name='rules-django'),
]
