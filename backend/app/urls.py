from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app import settings
from shop import views
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('cart', include('cart.urls', namespace='cart')),
    path('users/', include('users.urls', namespace='users')),
    path('recommend/', include('recommend.urls', namespace='recommend')),
    path('api/v1/', include('api.urls', namespace='api')),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found