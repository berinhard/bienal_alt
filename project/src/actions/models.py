from django.db import models
from django.utils.translation import gettext as _


class QuestionTag(models.Model):
    title = models.CharField(max_length=30, verbose_name=_("Texto da pergunta"))

    class Meta:
        verbose_name = _('Pergunta')
        verbose_name_plural = _('Perguntas')


class Action(models.Model):
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    title = models.CharField(max_length=100, verbose_name=_("Título"))
    body = models.TextField(verbose_name=_('Conteúdo HTML'), null=False, blank=False)
    js_code = models.TextField(blank=True, default='', verbose_name=_('Código Javascript'))
    custom_css = models.TextField(blank=True, default='', verbose_name=_('CSS Customizado'))
    extra_head = models.TextField(blank=True, default='', verbose_name=_('Extra head'))
    questions = models.ManyToManyField(QuestionTag, related_name='actions', verbose_name=_('Conteúdo HTML'))

    class Meta:
        verbose_name = _('Ação')
        verbose_name_plural = _('Ações')
