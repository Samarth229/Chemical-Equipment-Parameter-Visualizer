import sys
import requests
import json
import webbrowser
from requests.auth import HTTPBasicAuth

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QTextEdit,
    QVBoxLayout
)

# 🔹 Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

UPLOAD_API_URL = "http://127.0.0.1:8000/api/upload-csv/"
HISTORY_API_URL = "http://127.0.0.1:8000/api/history/"
PDF_API_URL = "http://127.0.0.1:8000/api/report/"

# 🔐 BASIC AUTH
AUTH = HTTPBasicAuth("Fossee", "fossee123")


class CsvUploader(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(200, 200, 720, 850)

        self.file_path = None
        self.chart_canvas = None
        self.latest_report_id = None

        # ---------- UI ELEMENTS ----------

        self.label = QLabel("Select a CSV file and upload it to backend")

        self.select_btn = QPushButton("Select CSV File")
        self.select_btn.clicked.connect(self.select_file)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_file)

        self.output_label = QLabel("Latest Summary")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(150)

        self.download_btn = QPushButton("Download PDF")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_pdf)

        self.chart_label = QLabel("Equipment Type Distribution")

        self.history_label = QLabel("Upload History (Last 5)")
        self.history_output = QTextEdit()
        self.history_output.setReadOnly(True)
        self.history_output.setMinimumHeight(250)

        # ---------- LAYOUT ----------

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.select_btn)
        self.layout.addWidget(self.upload_btn)
        self.layout.addWidget(self.output_label)
        self.layout.addWidget(self.output)
        self.layout.addWidget(self.download_btn)
        self.layout.addWidget(self.chart_label)
        self.layout.addWidget(self.history_label)
        self.layout.addWidget(self.history_output)

        self.setLayout(self.layout)

        # Load history on startup
        self.fetch_history()

    # ---------- FILE SELECTION ----------

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )

        if file_path:
            self.file_path = file_path
            self.label.setText(f"Selected file:\n{file_path}")

    # ---------- CSV UPLOAD ----------

    def upload_file(self):
        if not self.file_path:
            self.output.setText("❌ Please select a CSV file first")
            return

        try:
            with open(self.file_path, "rb") as f:
                response = requests.post(
                    UPLOAD_API_URL,
                    files={"file": f},
                    auth=AUTH
                )

            if response.status_code == 200:
                data = response.json()
                self.output.setText(json.dumps(data, indent=2))

                # Create chart
                self.create_chart(data.get("type_distribution", {}))

                # Refresh history
                self.fetch_history()

            else:
                self.output.setText(
                    f"❌ Error {response.status_code}\n{response.text}"
                )

        except Exception as e:
            self.output.setText(f"❌ Exception occurred:\n{str(e)}")

    # ---------- PDF DOWNLOAD ----------

    def download_pdf(self):
        if not self.latest_report_id:
            return

        url = f"{PDF_API_URL}{self.latest_report_id}/"
        webbrowser.open(url)

    # ---------- MATPLOTLIB CHART ----------

    def create_chart(self, type_distribution):
        if self.chart_canvas:
            self.layout.removeWidget(self.chart_canvas)
            self.chart_canvas.deleteLater()

        figure = Figure(figsize=(7, 4))
        self.chart_canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        equipment = list(type_distribution.keys())
        counts = list(type_distribution.values())

        ax.bar(equipment, counts)
        ax.set_title("Equipment Type Distribution")
        ax.set_xlabel("Equipment Type")
        ax.set_ylabel("Count")
        ax.set_xticklabels(equipment, rotation=45, ha="right")

        figure.tight_layout()
        self.layout.insertWidget(6, self.chart_canvas)

    # ---------- FETCH HISTORY ----------

    def fetch_history(self):
        try:
            response = requests.get(
                HISTORY_API_URL,
                auth=AUTH
            )

            if response.status_code == 200:
                history = response.json()
                display_text = ""

                if history:
                    self.latest_report_id = history[0]["id"]
                    self.download_btn.setEnabled(True)

                for item in history:
                    display_text += f"ID: {item['id']}\n"
                    display_text += f"Uploaded at: {item['uploaded_at']}\n"
                    display_text += json.dumps(item["summary"], indent=2)
                    display_text += "\n\n" + "-" * 40 + "\n\n"

                self.history_output.setText(display_text)

            else:
                self.history_output.setText("❌ Failed to fetch history")

        except Exception as e:
            self.history_output.setText(f"❌ Error:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CsvUploader()
    window.show()
    sys.exit(app.exec_())






