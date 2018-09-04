from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^mce_filebrowser/', include('src.mce_filebrowser.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^sobre/$', TemplateView.as_view(template_name='about.html'), name='about'),
    path('', include('src.actions.urls')),
    prefix_default_language=True,
)

if not settings.PRODUCTION:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
