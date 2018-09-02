from django import template
from django.conf import settings
from django.urls import resolve, reverse
from django.template.defaultfilters import safe
from django.utils import translation

register = template.Library()

@register.simple_tag
def trans_field(obj, fieldname, language_code):
    value = getattr(obj, fieldname)

    if language_code.upper() == settings.LANGUAGE_CODE.upper():
        return value
    elif language_code == 'en':
        trans_fieldname = fieldname + '_en'
        trans_value = getattr(obj, trans_fieldname, '')
        if trans_value:
            value = trans_value

    return value


@register.simple_tag
def trans_safe_field(*args, **kwargs):
    value = trans_field(*args, **kwargs)
    return safe(value)


@register.simple_tag
def trans_upper_field(*args, **kwargs):
    value = trans_field(*args, **kwargs)
    return value.upper()


class TranslatedURL(template.Node):

    def __init__(self, language):
        self.language = language

    def render(self, context):
        request = context['request']
        translation.activate(request.LANGUAGE_CODE)
        view = resolve(context['request'].path)
        translation.activate(self.language)
        url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        return url


@register.tag
def translate_url(parser, token):
    language = token.split_contents()[1]
    return TranslatedURL(language)
