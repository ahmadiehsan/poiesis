from django.urls import path

from .views import SelectFrameworkView, ReactView, DjangoView

app_name = 'naming'

urlpatterns = [
    path('', SelectFrameworkView.as_view(), name='select-framework'),
    path('react/', ReactView.as_view(), name='react'),
    path('django/', DjangoView.as_view(), name='django'),
]
