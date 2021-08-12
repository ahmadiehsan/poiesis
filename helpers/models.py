import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Create Time"))
    modify_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("is Deleted"))
    auto_cols = ['create_time', 'modify_time', 'is_deleted']

    def save(self, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(**kwargs)

    class Meta:
        ordering = ('-create_time',)
        get_latest_by = ('create_time',)
        abstract = True
