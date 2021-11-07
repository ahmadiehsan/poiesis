from django.db import models
from django.utils.translation import ugettext as _


class TaskPOChoices(models.IntegerChoices):
    task_description = 1, _('Task description'),  # توضیحات کامل تسک
    zeppelin_file_links = 2, _('Zeppelin file links'),  # لینک فایل طرح zeppelin
    permissions = 3, _('Task permissions'),  # دسترسی ها
    inputs_value = 4, _('Inputs value'),  # مقدارهای ورودی
    inputs_type = 5, _('Inputs type'),  # نوع ورودی ها
    related_tasks = 6, _('Related tasks'),  # تسک های درگیر شده
    backend_description = 7, _('Backend description'),  # ملاحظات بک اندی
    frontend_description = 8, _('Frontend description'),  # ملاحظات فرانتی
    test_cases = 9, _('Test cases'),  # تست کیس ها
