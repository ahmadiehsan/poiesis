from django.urls import path

from ..views import PORulesView, POTaskView

urlpatterns = [
    path('rules/', PORulesView.as_view(), name='po-rules'),
    path('task/', POTaskView.as_view(), name='po-task'),
]
