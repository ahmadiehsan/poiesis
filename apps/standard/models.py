from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import BaseModel


class RuleTopic(BaseModel):
    class Framework(models.IntegerChoices):
        REACT = 1, _('react')
        DJANGO = 2, _('django')

    title = models.CharField(verbose_name=_('title'), max_length=20)
    framework = models.IntegerField(verbose_name=_('framework'), choices=Framework.choices)

    def __str__(self):
        return f'{self.title} - {self.get_framework_display()}'

    class Meta:
        verbose_name = _('rule topic')
        verbose_name_plural = _('rule topics')


class RuleItem(BaseModel):
    class ItemType(models.IntegerChoices):
        CODING = 1, _('coding')
        TESTING = 2, _('testing')

    item_type = models.IntegerField(verbose_name=_('item type'), choices=ItemType.choices)
    content = models.TextField(verbose_name=_('content'))
    is_new = models.BooleanField(verbose_name=_('is new'), default=False)
    topic = models.ForeignKey(RuleTopic, verbose_name=_('topic'), on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f'{self.content[:15]} ...'

    class Meta:
        verbose_name = _('rule item')
        verbose_name_plural = _('rule items')
