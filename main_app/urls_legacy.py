from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path(
        'naming/react/',
        RedirectView.as_view(url=reverse_lazy('standard:naming-react'), permanent=True),
        name='home'
    ),
    path(
        'naming/django/',
        RedirectView.as_view(url=reverse_lazy('standard:naming-django'), permanent=True),
        name='home'
    ),
    path(
        'standard/coding/react/',
        RedirectView.as_view(url=reverse_lazy('standard:coding-and-testing-react'), permanent=True),
        name='coding-react'
    ),
    path(
        'standard/testing/react/',
        RedirectView.as_view(url=reverse_lazy('standard:coding-and-testing-react'), permanent=True),
        name='testing-react'
    ),
]
