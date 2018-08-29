from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

from tinymce.models import HTMLField
from yamlfield.fields import YAMLField


class QuestionTag(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Pergunta"))
    description = models.TextField(default='', verbose_name=_("Descrição"))
    title_en = models.CharField(max_length=100, verbose_name=_("Pergunta (EN)"), default='', blank=True)
    description_en = models.TextField(default='', verbose_name=_("Descrição (EN)"), blank=True)

    class Meta:
        verbose_name = _('Pergunta')
        verbose_name_plural = _('Perguntas')

    def __str__(self):
        return self.title

    @property
    def filter_url(self):
        return reverse('index') + '?question={}'.format(self.id)


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
    title_en = models.CharField(max_length=100, verbose_name=_("Título (EN)"), blank=True)
    body = HTMLField(verbose_name=(_("Conteúdo")))
    body_en = HTMLField(verbose_name=(_("Conteúdo (EN)")), default='', blank=True)
    js_code = models.TextField(blank=True, default='', verbose_name=_('Código Javascript'))
    custom_css = models.TextField(blank=True, default='', verbose_name=_('CSS Customizado'))
    extra_head = models.TextField(blank=True, default='', verbose_name=_('Extra head'))
    questions = models.ManyToManyField(QuestionTag, related_name='actions', verbose_name=_('Perguntas'))
    published = models.BooleanField(default=False, verbose_name=_('Publicada'))

    class Meta:
        verbose_name = _('Ação')
        verbose_name_plural = _('Ações')
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def detail_url(self):
        return reverse('detail', args=[self.slug])

    @property
    def preview_url(self):
        return reverse('preview', args=[self.slug])

    @property
    def has_carousel(self):
        return self.carousel.exists()

    @property
    def carousel_url(self):
        if not self.has_carousel:
            return ''
        return reverse('action_carousel', args=[self.slug])


class AnalyzedImage(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Nome"))
    title_en = models.CharField(max_length=100, verbose_name=_("Nome (EN)"), default='', blank=True)
    author = models.CharField(max_length=100, verbose_name=_("Autor"))
    date = models.DateField(verbose_name=_("Data"))
    action = models.ForeignKey(Action, related_name='carousel', on_delete=models.CASCADE, verbose_name=_('Ação'))
    image = models.ImageField(upload_to='carousel/', null=False, blank=False, verbose_name=_('Imagem'))
    info = YAMLField(default='', verbose_name=_('Resultados da Análise'))
    info_en = YAMLField(default='', verbose_name=_('Resultados da Análise (EN)'), blank=True)
    order = models.PositiveIntegerField(verbose_name=_('Posição'), default=1)

    class Meta:
        verbose_name = _('Imagem Analisada')
        verbose_name_plural = _('Imagens Analisadas')
        ordering = ['order']

    @property
    def analysis(self):
        return self.info.get('analise') or []

    @property
    def products(self):
        return self.info.get('produtos') or []

    @property
    def category(self):
        return self.info.get('categoria') or ''

    @property
    def thumbnails(self):
        return self.info.get('thumbnails') or self.info_en.get('thumbnails') or []

    @property
    def analysis_en(self):
        return self.info_en.get('analise') or []

    @property
    def products_en(self):
        return self.info_en.get('produtos') or []

    @property
    def category_en(self):
        return self.info_en.get('categoria') or ''


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Nome'))
    email = models.EmailField(verbose_name=_('E-mail'))
    message = models.TextField(verbose_name=_('Mensagem'))
    upload = models.FileField(upload_to='contacts/', null=True, blank=True, verbose_name=_('Envio de Arquivo'))
    date = models.DateField(auto_now_add=True, verbose_name=_('Data'))

    class Meta:
        verbose_name = _('Contato')
        verbose_name_plural = _('Contatos')
        ordering = ['-date']

    def __str__(self):
        return "{} - {}".format(self.name, self.email)
