from django import forms
from django.utils.translation import ugettext as _

from ..enums import POTaskChoices


class POTaskForm(forms.Form):
    task_title = forms.CharField(label=_('Task Title'))
    task_choices = forms.MultipleChoiceField(
        label=_('Task Choices'),
        widget=forms.CheckboxSelectMultiple(attrs={'checked': 'checked'}),
        choices=POTaskChoices.choices
    )
