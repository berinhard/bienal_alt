from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext as _

from src.actions.forms import ActionAdminForm
from src.actions.models import QuestionTag, Action, Contact


class QuestionTagAdmin(admin.ModelAdmin):
    list_display_links = None

    def has_delete_permission(self, request, obj=None):
        return False


class ActionAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'show_preview_url']
    actions = ['make_published']
    form = ActionAdminForm
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'questions', 'action_date', 'slug', 'published')
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('custom_css', 'js_code', 'extra_head'),
        }),
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
    readonly_fields = ['name', 'email', 'message', 'upload']

    def truncated_message(self, obj):
        msg = obj.message
        if len(msg) > 140:
            msg = msg[:140] + '...'
        return msg
    truncated_message.short_description = _("Mensagem")


#admin.site.register(QuestionTag, QuestionTagAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Contact, ContactAdmin)
