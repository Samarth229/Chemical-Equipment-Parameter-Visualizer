from django.urls import path
from .views import hello_api, upload_csv, upload_history
from .views import generate_pdf_report


urlpatterns = [
    path('hello/', hello_api),
    path('upload-csv/', upload_csv),
    path('history/', upload_history),
    path("report/<int:report_id>/", generate_pdf_report),
]
