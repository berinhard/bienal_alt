from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from suit.admin import SortableTabularInline

from src.actions.forms import ActionAdminForm, AnalyzedImageAdminForm
from src.actions.models import QuestionTag, Action, Contact, AnalyzedImage


class QuestionTagAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
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
    change_form_template = 'admin/actions_action_change_form.html'
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'questions', 'slug', 'published'),
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
    search_fields = ['title']

    def show_preview_url(self, obj):
        return format_html("<a href='{url}' target='_blank'>{url}</a>", url=obj.preview_url)
    show_preview_url.short_description = _("Preview")

    def make_published(self, request, queryset):
        queryset.update(published=True)
    make_published.short_description = _('Publica as ações')

    def response_change(self, request, obj):
        response = super().response_change(request, obj)
        if "_preview" in request.POST:
            return HttpResponseRedirect(obj.preview_url)
        if "_publish" in request.POST:
            obj.published = True
            obj.save()
            self.message_user(
                request,
                'A ação "{}" foi salva e publicada com sucesso!'.format(obj.title),
                messages.SUCCESS
            )
            return HttpResponseRedirect(reverse('admin:actions_action_changelist'))
        else:
            return response


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'truncated_message', 'upload']
    readonly_fields = ['name', 'email', 'message', 'date', 'upload']

    def truncated_message(self, obj):
        msg = obj.message
        if len(msg) > 140:
            msg = msg[:140] + '...'
        return msg
    truncated_message.short_description = _("Mensagem")


admin.site.register(QuestionTag, QuestionTagAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Contact, ContactAdmin)
