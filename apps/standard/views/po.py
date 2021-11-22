from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from ..enums import POTaskChoices
from ..forms import POTaskForm
from ..models import RuleTopic
from ..services import MarkdownService


class PORulesView(TemplateView):
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


class POTaskView(FormView):
    template_name = 'standard/task.html'
    form_class = POTaskForm
    success_url = reverse_lazy('standard:po-task')

    def form_valid(self, form):
        md_service = MarkdownService(file_name='task', title=form.data['task_title'])

        for task_choice in form.data.getlist('task_choices'):
            md_service.file.new_header(level=2, title=dict(POTaskChoices.choices)[int(task_choice)])
            md_service.file.new_line('توضیحات این بخش را اینجا وارد نمایید')
            md_service.file.new_line('\n\n')

        response = HttpResponse(
            md_service.read_file(),
            content_type='text/markdown',
            headers={'Content-Disposition': f'attachment; filename="task.md"'},
        )
        return response
