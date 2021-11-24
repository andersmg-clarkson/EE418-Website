from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.default, name="default"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('frontend/', include(('frontend.urls', 'frontend'), namespace='frontend')),
]
