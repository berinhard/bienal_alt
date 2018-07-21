from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext as _

from suit.admin import SortableTabularInline

from src.actions.forms import ActionAdminForm, AnalyzedImageAdminForm
from src.actions.models import QuestionTag, Action, Contact, AnalyzedImage


class QuestionTagAdmin(admin.ModelAdmin):
    list_display_links = None

    def has_delete_permission(self, request, obj=None):
        return False


class AnalyzedImageInline(SortableTabularInline):
    model = AnalyzedImage
    sortable = 'order'
    extra = 1
    suit_classes = 'suit-tab suit-tab-carousel'
    form = AnalyzedImageAdminForm


class ActionAdmin(admin.ModelAdmin):
    suit_form_tabs = (('acao', _('Ação')), ('carousel', _('Carrossel de Imagens')))
    suit_form_includes = (
        ('admin/carousel_helper.html', 'top', 'carousel'),
    )
    list_display = ['title', 'published', 'show_preview_url']
    inlines = [AnalyzedImageInline]
    actions = ['make_published']
    form = ActionAdminForm
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'questions', 'action_date', 'slug', 'published'),
            'classes': ('suit-tab', 'suit-tab-acao',),
        }),
        (_('Avançados'), {
            'classes': ('collapse', 'suit-tab', 'suit-tab-acao',),
            'fields': ('custom_css', 'js_code', 'extra_head'),
        }),
        (_('Carrossel de Imagens'), {
            'classes': ('suit-tab', 'suit-tab-carousel',),
            'fields': []
        })
    )
    prepopulated_fields = {'slug': ['title']}
    list_filter = ['questions', 'published']

    def show_preview_url(self, obj):
        return format_html("<a href='{url}' target='_blank'>{url}</a>", url=obj.preview_url)
    show_preview_url.short_description = _("Preview")

    def make_published(self, request, queryset):
        queryset.update(published=True)
    make_published.short_description = _('Publica as ações')


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'truncated_message', 'upload']
    readonly_fields = ['name', 'email', 'message', 'date', 'upload']

    def truncated_message(self, obj):
        msg = obj.message
        if len(msg) > 140:
            msg = msg[:140] + '...'
        return msg
    truncated_message.short_description = _("Mensagem")


#admin.site.register(QuestionTag, QuestionTagAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Contact, ContactAdmin)
