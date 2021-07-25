from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path(
        'naming/react/',
        RedirectView.as_view(url=reverse_lazy('standard:naming-react'), permanent=False),
        name='home'
    ),
    path(
        'naming/django/',
        RedirectView.as_view(url=reverse_lazy('standard:naming-django'), permanent=False),
        name='home'
    ),
]
