from django.views.generic import TemplateView

from main_app.settings import BASE_DIR


class SelectFrameworkView(TemplateView):
    template_name = 'standard/select_framework.html'


class NamingReactView(TemplateView):
    template_name = 'standard/naming.html'

    @staticmethod
    def _generate_pages(entity):
        return (
            [
                f'{entity}FormPage.js',
                f'{entity}SinglePage.js',
                f'{entity}ListPage.js',
            ],
            ''
        )

    @staticmethod
    def _generate_actions(entity):
        return (
            [
                f'{entity}Create = () => {{}};',
                f'{entity}Get = () => {{}};',
                f'{entity}List = () => {{}};',
                f'{entity}Delete = () => {{}};',
                f'{entity}Update = () => {{}};',
            ],
            ''
        )

    @staticmethod
    def _generate_action_types(entity):
        action_type = f'{entity.upper()}_TYPES'
        return (
            [
                f'{action_type}.get',
                f'{action_type}.loading',
                f'{action_type}.error',
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
            'title_fa': 'ری‌اکت'
        })

        return context


class NamingDjangoView(TemplateView):
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

            context.update({
                'entity': entity,
                'rules': {
                    'models.py': {'names': models_names, 'help_code': models_help_code},
                    'views.py': {'names': views_names, 'help_code': views_help_code},
                    'serializers.py': {'names': serializers_names, 'help_code': serializers_help_code},
                    'validators.py': {'names': validators_names, 'help_code': validators_help_code},
                    'services.py': {'names': services_names, 'help_code': services_help_code},
                }
            })
        else:
            context.update({
                'entity': '',
            })

        context.update({
            'title_en': 'Django',
            'title_fa': 'جنگو'
        })

        return context


class CodingReactView(TemplateView):
    template_name = 'standard/coding.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with open(BASE_DIR / 'apps' / 'standard' / 'templates' / 'standard' / '_react_coding_rules.html', 'r') as file:
            context.update({
                'title_en': 'React',
                'title_fa': 'ری‌اکت',
                'text': file.read()
            })

        return context
