from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('apps.works.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('messages/', include('apps.messages_app.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('orders/', include('apps.orders.urls')),
    path('map/', include('apps.map_app.urls')),
    path('admin-panel/', include('apps.admin_panel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
