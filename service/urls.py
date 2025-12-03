from django.views.generic import RedirectView
from xml.etree.ElementInclude import include
from django.conf.urls.static import static
from django.conf  import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('enumeration/', include('enumeration.urls')),
    path('', RedirectView.as_view(url='enumeration/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)