from django.db import models
from django.db.models.query import QuerySet


class PublishQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None):
        super(PublishQuerySet, self).__init__(model, query)

    def published(self, **kwargs):
        return self.filter(is_published=True, **kwargs)

    def visible(self, **kwargs):
        return self.published(**kwargs)


class PublishManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return PublishQuerySet(self.model)

    def published(self, *args, **kwargs):
        return self.get_query_set().published(*args, **kwargs)


class PublishModel(models.Model):
    is_published = models.BooleanField(verbose_name='публикация', default=True)

    objects = PublishManager()

    class Meta:
        abstract = True
