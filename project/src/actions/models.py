from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

from tinymce.models import HTMLField


class QuestionTag(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("Texto da pergunta"))

    class Meta:
        verbose_name = _('Pergunta')
        verbose_name_plural = _('Perguntas')

    def __str__(self):
        return self.title


class ActionQuerySet(models.QuerySet):

    def search(self, search_query):
        return self.filter(
            models.Q(title__icontains=search_query) |
            models.Q(body__icontains=search_query)
        )

    def published(self):
        return self.filter(published=True)


class Action(models.Model):
    objects = ActionQuerySet.as_manager()

    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    title = models.CharField(max_length=100, verbose_name=_("Título"))
    body = HTMLField()
    js_code = models.TextField(blank=True, default='', verbose_name=_('Código Javascript'))
    custom_css = models.TextField(blank=True, default='', verbose_name=_('CSS Customizado'))
    extra_head = models.TextField(blank=True, default='', verbose_name=_('Extra head'))
    questions = models.ManyToManyField(QuestionTag, related_name='actions', verbose_name=_('Perguntas'))
    action_date = models.DateField(verbose_name=_('Data da ação'))
    published = models.BooleanField(default=False, verbose_name=_('Publicada'))

    class Meta:
        verbose_name = _('Ação')
        verbose_name_plural = _('Ações')

    def __str__(self):
        return self.title

    @property
    def detail_url(self):
        return reverse('detail', args=[self.slug])

    @property
    def preview_url(self):
        return reverse('preview', args=[self.slug])
