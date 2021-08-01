from django.urls import path

from .views import SelectFrameworkView, NamingReactView, NamingDjangoView, CodingReactView, TestingReactView

app_name = 'standard'

urlpatterns = [
    path('', SelectFrameworkView.as_view(), name='select-framework'),
    path('naming/react/', NamingReactView.as_view(), name='naming-react'),
    path('naming/django/', NamingDjangoView.as_view(), name='naming-django'),
    path('coding/react/', CodingReactView.as_view(), name='coding-react'),
    path('testing/react/', TestingReactView.as_view(), name='testing-react'),
]
