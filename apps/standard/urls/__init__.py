from django.urls import path, include

app_name = 'standard'

urlpatterns = [
    path('', include('apps.standard.urls.generic')),
    path('po/', include('apps.standard.urls.po')),
    path('django/', include('apps.standard.urls.django')),
    path('react/', include('apps.standard.urls.react')),
]
