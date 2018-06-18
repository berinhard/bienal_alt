from django.conf.urls import url

from src.actions.views import ListActionsView


urlpatterns = [
    url(r'', ListActionsView.as_view(), name='index'),
]
