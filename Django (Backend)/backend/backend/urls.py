from django.contrib import admin
from django.urls import path, include
from equipment.views import hello_api, upload_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hello/', hello_api),
    path('api/upload-csv/', upload_csv),
    path('api/', include('equipment.urls')),
]
