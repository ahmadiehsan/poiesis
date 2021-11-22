from django.urls import path

from ..views import SelectStandardView

urlpatterns = [
    path('', SelectStandardView.as_view(), name='select-standard'),
]
