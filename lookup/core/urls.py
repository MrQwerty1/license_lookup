from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0/', include(('api.v0.urls', 'api'), namespace='api_v0')),
]
