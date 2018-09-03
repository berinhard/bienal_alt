from django.conf import settings
from django.conf.urls import url
from django.urls import re_path
from django.views.decorators.cache import cache_page

from src.actions.views import *

timeout = settings.CACHE_DEFAULT_TIMEOUT


urlpatterns = [
    re_path(r'^$', cache_page(timeout, key_prefix="home")(ListActionsView.as_view()), name='index'),
    re_path(r'^contato/$', cache_page(timeout, key_prefix="contact")(AddContactView.as_view()), name='contact'),
    re_path(r'preview/(?P<slug>[\w-]+)/$', action_preview_view, name='preview'),
    re_path(r'acao/(?P<slug>[\w-]+)/$', action_detail_view, name='detail'),
    re_path(r'acao/(?P<slug>[\w-]+)/carrossel$', action_carousel_html, name='action_carousel'),
]
