import re

from django.views.generic import TemplateView

from .mixins import AnalysisFileGeneratorMixin
from ..models import RuleTopic


class ReactNamingView(TemplateView, AnalysisFileGeneratorMixin):
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


class ReactRulesView(TemplateView):
    template_name = 'standard/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title_en': 'React',
            'title_fa': 'ری‌اکت',
            'description': '(کدنویسی و تست)',
            'activate_filter': True,
            'rule_topics': RuleTopic.objects.filter(rule_type=RuleTopic.RuleType.REACT)
        })
        return context
