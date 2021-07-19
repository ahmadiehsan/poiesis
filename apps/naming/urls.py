from django.urls import path

from .views import SelectFramework

app_name = 'naming'

urlpatterns = [
    path('', SelectFramework.as_view(), name='reports'),
]
