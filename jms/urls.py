from django.contrib import admin
from django.urls import path, include
from app import urls as app_urls
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('app/', include(app_urls)),
]
