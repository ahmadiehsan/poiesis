from django.urls import path

from .views import SelectFramework

app_name = 'naming'

urlpatterns = [
    path('', SelectFramework.as_view(), name='select-framework'),
    path('react/', SelectFramework.as_view(), name='react'),
    path('python/', SelectFramework.as_view(), name='python'),
]
