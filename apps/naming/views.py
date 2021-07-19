from django.views.generic import TemplateView


class SelectFrameworkView(TemplateView):
    template_name = 'naming/select_framework.html'


class EntityView(TemplateView):
    template_name = 'naming/select_entity.html'


class ReactView(TemplateView):
    template_name = 'naming/select_framework.html'


class DjangoView(TemplateView):
    template_name = 'naming/select_framework.html'
