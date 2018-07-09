from django.contrib import admin
from django.utils.translation import gettext as _

from src.actions.forms import ActionAdminForm
from src.actions.models import QuestionTag, Action


class QuestionTagAdmin(admin.ModelAdmin):
    list_display_links = None

    def has_delete_permission(self, request, obj=None):
        return False


class ActionAdmin(admin.ModelAdmin):
    form = ActionAdminForm
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'questions', 'action_date', 'slug')
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('custom_css', 'js_code', 'extra_head'),
        }),
    )
    prepopulated_fields = {'slug': ['title']}
    list_filter = ['questions']


#admin.site.register(QuestionTag, QuestionTagAdmin)
admin.site.register(Action, ActionAdmin)
