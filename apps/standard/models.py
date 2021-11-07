from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import BaseModel


class RuleTopic(BaseModel):
    class RuleType(models.IntegerChoices):
        REACT = 1, _('React')
        DJANGO = 2, _('Django')
        PO = 3, _('PO')

    title = models.CharField(verbose_name=_('Title'), max_length=20)
    rule_type = models.IntegerField(verbose_name=_('Rule Type'), choices=RuleType.choices)

    def __str__(self):
        return f'{self.title} - {self.get_rule_type_display()}'

    class Meta:
        verbose_name = _('Rule Topic')
        verbose_name_plural = _('Rule Topics')


class RuleItem(BaseModel):
    class ItemType(models.IntegerChoices):
        CODING = 1, _('Coding')
        TESTING = 2, _('Testing')

    item_type = models.IntegerField(verbose_name=_('Item Type'), choices=ItemType.choices, null=True, blank=True)
    content = models.TextField(verbose_name=_('Content'))
    is_new = models.BooleanField(verbose_name=_('Is New'), default=False)
    topic = models.ForeignKey(RuleTopic, verbose_name=_('Topic'), on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f'{self.content[:15]} ...'

    class Meta:
        verbose_name = _('Rule Item')
        verbose_name_plural = _('Rule Items')
