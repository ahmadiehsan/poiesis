from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from .urls_legacy import urlpatterns as legacy_urlpatterns

urlpatterns = legacy_urlpatterns + [
    path('standard/', include('apps.standard.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('standard:select-standard'), permanent=False), name='home'),
]
