import pandas as pd

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes,
    authentication_classes,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from .models import UploadHistory


# -------------------------------
# Public API (No Authentication)
# -------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def hello_api(request):
    return Response({"message": "Backend is working!"})


# --------------------------------
# Protected API (Basic Auth)
# --------------------------------
@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    file = request.FILES.get("file")

    if not file:
        return Response(
            {"error": "No CSV file uploaded"},
            status=400
        )

    try:
        df = pd.read_csv(file)

        summary = {
            "total_equipment": int(len(df)),
            "avg_flowrate": round(df["Flowrate"].mean(), 2),
            "avg_pressure": round(df["Pressure"].mean(), 2),
            "avg_temperature": round(df["Temperature"].mean(), 2),
            "type_distribution": df["Type"].value_counts().to_dict(),
        }

        UploadHistory.objects.create(summary=summary)

        if UploadHistory.objects.count() > 5:
            UploadHistory.objects.order_by("uploaded_at").first().delete()

        return Response(summary)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=400
        )


# --------------------------------
# Protected API (Basic Auth)
# --------------------------------
@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def upload_history(request):
    history = UploadHistory.objects.order_by("-uploaded_at")[:5]

    data = [
    {
        "id": item.id,
        "uploaded_at": item.uploaded_at,
        "summary": item.summary,
    }
    for item in history
    ]


    return Response(data)


# --------------------------------
# PDF Report Generation (Basic Auth)
# --------------------------------
@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request, report_id):
    try:
        record = UploadHistory.objects.get(pk=report_id)
        summary = record.summary

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="equipment_report_{report_id}.pdf"'
        )

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        y = height - 50

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, "Chemical Equipment Analysis Report")
        y -= 40

        p.setFont("Helvetica", 11)
        p.drawString(50, y, f"Generated At: {record.uploaded_at}")
        y -= 30

        p.drawString(50, y, f"Total Equipment: {summary['total_equipment']}")
        y -= 20

        p.drawString(50, y, f"Average Flowrate: {summary['avg_flowrate']}")
        y -= 20

        p.drawString(50, y, f"Average Pressure: {summary['avg_pressure']}")
        y -= 20

        p.drawString(50, y, f"Average Temperature: {summary['avg_temperature']}")
        y -= 30

        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Equipment Type Distribution:")
        y -= 20

        p.setFont("Helvetica", 11)
        for eq_type, count in summary["type_distribution"].items():
            p.drawString(70, y, f"{eq_type}: {count}")
            y -= 18

            if y < 50:
                p.showPage()
                y = height - 50

        p.showPage()
        p.save()

        return response

    except UploadHistory.DoesNotExist:
        return Response(
            {"error": "Report not found"},
            status=404
        )




