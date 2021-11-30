from django.views.generic import TemplateView

from .mixins import AnalysisFileGeneratorMixin
from ..models import RuleTopic


class DjangoNamingView(TemplateView, AnalysisFileGeneratorMixin):
    template_name = 'standard/naming.html'

    @staticmethod
    def _generate_models(entity):
        return [f'class {entity}'], ''

    @staticmethod
    def _generate_views(entity):
        return (
            [
                f'class {entity}View',
            ],
            ''
        )

    @staticmethod
    def _generate_serializers(entity):
        return (
            [
                f'class Base{entity}Serializer',
                f'class {entity}Serializer',
                f'class {entity}ListSerializer',
                f'class {entity}MinimalSerializer',
            ],
            ''
        )

    @staticmethod
    def _generate_validators(entity):
        return [f'class {entity}Validator'], ''

    @staticmethod
    def _generate_services(entity):
        return [f'class {entity}Service'], ''

    @staticmethod
    def _generate_tests(entity):
        return (
            [
                f'class {entity}Test',
                f'class {entity}TestMixin',
            ],
            ''
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entity = self.request.GET.get('entity')
        if entity:
            entity = entity[0].upper() + entity[1:]

            models_names, models_help_code = self._generate_models(entity)
            views_names, views_help_code = self._generate_views(entity)
            serializers_names, serializers_help_code = self._generate_serializers(entity)
            validators_names, validators_help_code = self._generate_validators(entity)
            services_names, services_help_code = self._generate_services(entity)
            tests_names, tests_help_code = self._generate_tests(entity)

            context.update({
                'entity': entity,
                'rules': {
                    'models.py': {'names': models_names, 'help_code': models_help_code},
                    'views.py': {'names': views_names, 'help_code': views_help_code},
                    'serializers.py': {'names': serializers_names, 'help_code': serializers_help_code},
                    'validators.py': {'names': validators_names, 'help_code': validators_help_code},
                    'services.py': {'names': services_names, 'help_code': services_help_code},
                    'tests.py': {'names': tests_names, 'help_code': tests_help_code},
                }
            })
        else:
            context.update({
                'entity': '',
            })

        context.update({
            'title_en': 'Django',
            'title_fa': 'جنگو',
            'analysis_mode': True if self.request.GET.get('analysis-mode') == 'on' else False
        })

        return context


class DjangoRulesView(TemplateView):
    template_name = 'standard/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title_en': 'Django',
            'title_fa': 'جنگو',
            'description': '(کدنویسی و تست)',
            'activate_filter': True,
            'rule_topics': RuleTopic.objects.filter(rule_type=RuleTopic.RuleType.DJANGO)
        })
        return context
