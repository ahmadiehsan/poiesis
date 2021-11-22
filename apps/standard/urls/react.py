from django.urls import path

from ..views import ReactNamingView, ReactRulesView

urlpatterns = [
    path('naming/', ReactNamingView.as_view(), name='react-naming'),
    path('rules/', ReactRulesView.as_view(), name='react-rules'),
]
