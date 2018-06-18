from django.conf.urls import url
from django.urls import re_path

from src.actions.views import ListActionsView, action_detail_view


urlpatterns = [
    re_path(r'^$', ListActionsView.as_view(), name='index'),
    re_path(r'(?P<slug>[\w-]+)/$', action_detail_view, name='detail'),
]
