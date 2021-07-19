from django.views.generic import TemplateView


class SelectFrameworkView(TemplateView):
    template_name = 'naming/select_framework.html'


class EntityView(TemplateView):
    template_name = 'naming/select_entity.html'


class ReactView(TemplateView):
    template_name = 'naming/react.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entity = self.request.GET.get('entity')
        context.update({'entity': entity})
        return context


class DjangoView(TemplateView):
    template_name = 'naming/django.html'

    @staticmethod
    def _generate_models(entity):
        return [f'class {entity}']

    @staticmethod
    def _generate_views(entity):
        return [
            f'class {entity}ViewSet --- DRF only',
            f'class {entity}APIView --- DRF only',
            f'class {entity}View --- Django only',
        ]

    @staticmethod
    def _generate_serializers(entity):
        return [
            f'class {entity}Serializer',
            f'class {entity}ListSerializer',
            f'class {entity}MinimalSerializer',
            f'class {entity}ReadOnlySerializer',
        ]

    @staticmethod
    def _generate_validators(entity):
        return [f'class {entity}Validator']

    @staticmethod
    def _generate_services(entity):
        return [f'class {entity}Service']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entity = self.request.GET.get('entity')
        entity = entity[0].upper() + entity[1:]
        context.update({
            'entity': entity,
            'models': self._generate_models(entity),
            'views': self._generate_views(entity),
            'serializers': self._generate_serializers(entity),
            'validators': self._generate_validators(entity),
            'services': self._generate_services(entity),
        })
        return context
