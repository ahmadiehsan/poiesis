from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView


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
                            'url': f"{reverse('standard:react-naming')}?analysis-mode=on"
                        },
                        {
                            'title': _('Naming'),
                            'url': reverse('standard:react-naming')
                        },
                        {
                            'title': _('Code and test'),
                            'url': reverse('standard:react-rules')
                        },
                    ],
                },
                {
                    'title': _('Django'),
                    'image_address': 'standard/images/django.jpg',
                    'links': [
                        {
                            'title': _('Analysis'),
                            'url': f"{reverse('standard:django-naming')}?analysis-mode=on"
                        },
                        {
                            'title': _('Naming'),
                            'url': reverse('standard:django-naming')
                        },
                        {
                            'title': _('Code and test'),
                            'url': reverse('standard:django-rules')
                        },
                    ],
                },
                {
                    'title': _('PO'),
                    'image_address': 'standard/images/po.jpg',
                    'links': [
                        {
                            'title': _('Negative Point'),
                            'url': reverse('standard:po-rules')
                        },
                        {
                            'title': _('Task'),
                            'url': reverse('standard:po-task')
                        },
                    ],
                },
            ]
        })

        return context
