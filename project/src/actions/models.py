from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

from tinymce.models import HTMLField
from yamlfield.fields import YAMLField


class QuestionTag(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("Texto da pergunta"))

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

    @property
    def has_carousel(self):
        return self.carousel.exists()


class AnalyzedImage(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Nome"))
    author = models.CharField(max_length=100, verbose_name=_("Autor"))
    date = models.DateField(verbose_name=_("Data"), auto_now_add=True)
    action = models.ForeignKey(Action, related_name='carousel', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='carousel/', null=False, blank=False, verbose_name=_('Imagem'))
    info = YAMLField(default='', verbose_name=_('Resultados da Análise'))
    order = models.PositiveIntegerField(verbose_name=_('Posição'))

    class Meta:
        verbose_name = _('Imagem Analisada')
        verbose_name_plural = _('Imagens Analisadas')
        ordering = ['order']

    @property
    def analysis(self):
        return self.info['analise']

    @property
    def products(self):
        return self.info['produtos']

    @property
    def category(self):
        return self.info['categoria']


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
