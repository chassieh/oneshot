from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Shot at a Deal Administration'
admin.site.site_title = 'Shot at a Deal Admin'
admin.site.index_title = 'Shot at a Deal Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('submissions/', include('submissions.urls')),
    path('producers/', include('producers.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
