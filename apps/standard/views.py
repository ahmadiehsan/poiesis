import re
from copy import deepcopy

from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, FormView

from .enums import TaskPOChoices
from .forms import TaskPOForm
from .models import RuleTopic
from .services import MarkdownService


class SelectStandardView(TemplateView):
    template_name = 'standard/select_standard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'standards': [
                {
                    'title': _('React'),
                    'image_address': 'standard/images/react.jpg',
                    'links': [
                        {
                            'title': _('Analysis'),
                            'url': f"{reverse('standard:naming-react')}?analysis-mode=on"
                        },
                        {
                            'title': _('Naming'),
                            'url': reverse('standard:naming-react')
                        },
                        {
                            'title': _('Code and test'),
                            'url': reverse('standard:rules-react')
                        },
                    ],
                },
                {
                    'title': _('Django'),
                    'image_address': 'standard/images/django.jpg',
                    'links': [
                        {
                            'title': _('Analysis'),
                            'url': f"{reverse('standard:naming-django')}?analysis-mode=on"
                        },
                        {
                            'title': _('Naming'),
                            'url': reverse('standard:naming-django')
                        },
                        {
                            'title': _('Code and test'),
                            'url': reverse('standard:rules-django')
                        },
                    ],
                },
                {
                    'title': _('PO'),
                    'image_address': 'standard/images/po.jpg',
                    'links': [
                        {
                            'title': _('Negative Point'),
                            'url': reverse('standard:rules-po')
                        },
                        {
                            'title': _('Task'),
                            'url': reverse('standard:task-po')
                        },
                    ],
                },
            ]
        })

        return context


class AnalysisFileGeneratorMixin:
    def _get_clean_POST_data(self, request):
        data = deepcopy(request.POST)
        del data['csrfmiddlewaretoken']
        return data

    @staticmethod
    def _generate_md_file(standard_table_content, standard_dict):
        md_service = MarkdownService(file_name='analysis')
        md_service.file.new_header(level=1, title='عنوان تحلیل را اینجا وارد نمایید')

        md_service.file.new_line('\n')
        md_service.file.new_header(level=2, title='استاندارد نام گذاری')

        md_service.file.new_line()
        md_service.file.new_table(
            columns=2,
            rows=int(len(standard_table_content) / 2),
            text=standard_table_content,
            text_align='center'
        )

        md_service.file.new_line('\n')
        md_service.file.new_header(level=2, title='توضیح هر سطر جدول')

        for scope in standard_dict:
            md_service.file.new_header(level=3, title=scope)
            md_service.file.new_list(standard_dict[scope])
            md_service.file.new_line('توضیحات این بخش را اینجا وارد نمایید')
            md_service.file.new_line('\n\n')

        md_service.file.new_header(level=2, title='ابهامات')
        md_service.file.new_line('در صورت وجود ابهام و یا سوالی آنرا اینجا وارد نمایید')

        md_service.file.new_line('\n\n')
        md_service.file.new_header(level=2, title='دیگر توضیحات')
        md_service.file.new_line('هر توضیح دیگری که در قالب بالا جا نمی‌گیرد را اینجا وارد نمایید')

        return md_service

    def post(self, request):
        standard_table_content = ['فایل/مفهوم', 'مقدار']
        standard_dict = {}
        for scope in self._get_clean_POST_data(request):
            for value in request.POST.getlist(scope):
                standard_table_content.extend([scope, value])
                standard_dict.setdefault(scope, []).append(value)

        md_service = self._generate_md_file(standard_table_content, standard_dict)

        response = HttpResponse(
            md_service.read_file(),
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
            'description': '(کدنویسی و تست)',
            'activate_filter': True,
            'rule_topics': RuleTopic.objects.filter(rule_type=RuleTopic.RuleType.REACT)
        })
        return context


class RulesDjangoView(TemplateView):
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


class RulesPOView(TemplateView):
    template_name = 'standard/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title_fa': 'نمره منفی',
            'activate_filter': False,
            'help_image': 'standard/images/po_rules.png',
            'rule_topics': RuleTopic.objects.filter(rule_type=RuleTopic.RuleType.PO)
        })
        return context


class TaskPOView(FormView):
    template_name = 'standard/task.html'
    form_class = TaskPOForm
    success_url = reverse_lazy('standard:task-po')

    def form_valid(self, form):
        md_service = MarkdownService(file_name='task', title=form.data['task_title'])

        for task_choice in form.data.getlist('task_choices'):
            md_service.file.new_header(level=2, title=dict(TaskPOChoices.choices)[int(task_choice)])
            md_service.file.new_line('توضیحات این بخش را اینجا وارد نمایید')
            md_service.file.new_line('\n\n')

        response = HttpResponse(
            md_service.read_file(),
            content_type='text/markdown',
            headers={'Content-Disposition': f'attachment; filename="task.md"'},
        )
        return response
