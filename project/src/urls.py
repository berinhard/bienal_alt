from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^sobre/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^contato/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^tinymce/', include('tinymce.urls')),
    path('', include('src.actions.urls')),
]
