from django import template
from django.conf import settings
from django.template.defaultfilters import safe

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
