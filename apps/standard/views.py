import re
from copy import deepcopy

from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import RuleTopic
from .services import AnalysisService


class SelectFrameworkView(TemplateView):
    template_name = 'standard/select_framework.html'


class AnalysisFileGeneratorMixin:
    def _get_clean_POST_data(self, request):
        data = deepcopy(request.POST)
        del data['csrfmiddlewaretoken']
        return data

    def post(self, request):
        standard_table_content = ['فایل/مفهوم', 'مقدار']
        standard_dict = {}
        for scope in self._get_clean_POST_data(request):
            for value in request.POST.getlist(scope):
                standard_table_content.extend([scope, value])
                standard_dict.setdefault(scope, []).append(value)

        service = AnalysisService()
        service.fill_file_with_default_content(standard_table_content, standard_dict)

        response = HttpResponse(
            service.read_file(),
            content_type='text/markdown',
            headers={'Content-Disposition': f'attachment; filename="analysis_{request.GET["entity"]}.md"'},
        )
        return response


class NamingReactView(TemplateView, AnalysisFileGeneratorMixin):
    template_name = 'standard/naming.html'

    @staticmethod
    def _generate_pages(entity):
        return (
            [
                f'{entity}FormPage.js',
                f'{entity}SinglePage.js',
                '---',
                f'{entity}ListPage.js',
            ],
            ''
        )

    @staticmethod
    def _generate_actions(entity):
        return (
            [
                f'{entity}Create',
                f'{entity}Get',
                f'{entity}Delete',
                f'{entity}Update',
                '---',
                f'{entity}List',
            ],
            ''
        )

    @staticmethod
    def _generate_action_types(entity):
        action_type = f"{re.sub(r'(?<!^)(?=[A-Z])', '_', entity).upper()}_TYPES"
        return (
            [
                f'{action_type}.get',
                f'{action_type}.loading',
                f'{action_type}.error',
                f'{action_type}.create',
                f'{action_type}.delete',
                f'{action_type}.update',
                '---',
                f'{action_type}.list.get',
                f'{action_type}.list.loading',
                f'{action_type}.list.error',
            ],
            f"""
            export const {action_type} = {{<br>
            &emsp;...actionTypeGenerator('{entity}')<br>
            }}
            """
        )

    @staticmethod
    def _generate_reducer(entity):
        return (
            [
                f'{entity}.data',
                f'{entity}.isLoading',
                f'{entity}.error',
                '---',
                f'{entity}.list.data',
                f'{entity}.list.isLoading',
                f'{entity}.list.error',
            ],
            """
            const initialState = {<br>
            &emsp;...stateGenerator()<br>
            }
            """
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entity = self.request.GET.get('entity')
        if entity:
            entity = entity[0].lower() + entity[1:]
            entity_capitalized = entity[0].upper() + entity[1:]

            pages_names, pages_help_code = self._generate_pages(entity_capitalized)
            actions_names, actions_help_code = self._generate_actions(entity)
            action_types_names, action_types_help_code = self._generate_action_types(entity)
            reducer_names, reducer_help_code = self._generate_reducer(entity)

            context.update({
                'entity': entity,
                'help_image': 'standard/images/react_entity_base.jpg',
                'rules': {
                    'Pages': {'names': pages_names, 'help_code': pages_help_code},
                    'Actions (Action Creators)': {'names': actions_names, 'help_code': actions_help_code},
                    'Action Types': {'names': action_types_names, 'help_code': action_types_help_code},
                    'Reducer': {'names': reducer_names, 'help_code': reducer_help_code},
                }
            })
        else:
            context.update({
                'entity': '',
            })

        context.update({
            'title_en': 'React',
            'title_fa': 'ری‌اکت',
            'analysis_mode': True if self.request.GET.get('analysis-mode') == 'on' else False
        })

        return context


class NamingDjangoView(TemplateView, AnalysisFileGeneratorMixin):
    template_name = 'standard/naming.html'

    @staticmethod
    def _generate_models(entity):
        return [f'class {entity}'], ''

    @staticmethod
    def _generate_views(entity):
        return (
            [
                f'class {entity}ViewSet --- DRF only',
                f'class {entity}APIView --- DRF only',
                f'class {entity}View --- Django only',
            ],
            ''
        )

    @staticmethod
    def _generate_serializers(entity):
        return (
            [
                f'class {entity}Serializer',
                f'class {entity}ListSerializer',
                f'class {entity}MinimalSerializer',
                f'class {entity}ReadOnlySerializer',
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


class RulesReactView(TemplateView):
    template_name = 'standard/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title_en': 'React',
            'title_fa': 'ری‌اکت',
            'rule_topics': RuleTopic.objects.filter(framework=RuleTopic.Framework.REACT)
        })
        return context


class RulesDjangoView(TemplateView):
    template_name = 'standard/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title_en': 'Django',
            'title_fa': 'جنگو',
            'rule_topics': RuleTopic.objects.filter(framework=RuleTopic.Framework.DJANGO)
        })
        return context
