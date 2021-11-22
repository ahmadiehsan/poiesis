from django.urls import path

from ..views import DjangoNamingView, DjangoRulesView

urlpatterns = [
    path('naming/', DjangoNamingView.as_view(), name='django-naming'),
    path('rules/', DjangoRulesView.as_view(), name='django-rules'),
]
