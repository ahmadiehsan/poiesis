from django.urls import path

from .views import (
    SelectFrameworkView,
    NamingReactView,
    NamingDjangoView,
    CodingAndTestingReactView,
    CodingAndTestingDjangoView
)

app_name = 'standard'

urlpatterns = [
    path('', SelectFrameworkView.as_view(), name='select-framework'),
    path('naming/react/', NamingReactView.as_view(), name='naming-react'),
    path('naming/django/', NamingDjangoView.as_view(), name='naming-django'),
    path('coding-and-testing/react/', CodingAndTestingReactView.as_view(), name='coding-and-testing-react'),
    path('coding-and-testing/django/', CodingAndTestingDjangoView.as_view(), name='coding-and-testing-django'),
]
