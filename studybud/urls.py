from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/', include('api.urls')),
    path('', include('base.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Studybuddy Admin'
admin.site.site_title = 'Studybuddy Admin'
# admin.site.index_title = 'Studybuddy Admin'
