from django.contrib.admin import register

from helpers.admin import BaseAdmin
from .models import RuleTopic, RuleItem


@register(RuleTopic)
class RuleTopicAdmin(BaseAdmin):
    list_display = ('title', 'rule_type')
    list_filter = ('rule_type',)
    search_fields = ('title',)


@register(RuleItem)
class RuleItemAdmin(BaseAdmin):
    list_display = ('__str__', 'topic', 'item_type', 'is_new')
    list_filter = ('item_type', 'is_new', 'topic__rule_type')
    search_fields = ('content',)
