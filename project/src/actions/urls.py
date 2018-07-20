from django.conf.urls import url
from django.urls import re_path

from src.actions.views import ListActionsView, action_detail_view, action_preview_view, AddContactView


urlpatterns = [
    re_path(r'^$', ListActionsView.as_view(), name='index'),
    re_path(r'^contato/$', AddContactView.as_view(), name='contact'),
    re_path(r'preview/(?P<slug>[\w-]+)/$', action_preview_view, name='preview'),
    re_path(r'(?P<slug>[\w-]+)/$', action_detail_view, name='detail'),
]
