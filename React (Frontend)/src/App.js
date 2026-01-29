import React, { useState, useEffect } from "react";
import "./App.css";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Bar } from "react-chartjs-2";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [error, setError] = useState("");

  // 🔐 BASIC AUTH (DEMO PURPOSE)
  const authHeader = {
    Authorization: "Basic " + btoa("Fossee:fossee123"),
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setError("");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a CSV file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/api/upload-csv/",
        {
          method: "POST",
          headers: authHeader,
          body: formData,
        }
      );

      if (!res.ok) {
        throw new Error("Unauthorized or upload failed");
      }

      const data = await res.json();
      setResult(data);
      fetchHistory();
    } catch (err) {
      setError("Failed to upload CSV (check authentication)");
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await fetch(
        "http://127.0.0.1:8000/api/history/",
        {
          headers: authHeader,
        }
      );

      if (!res.ok) {
        throw new Error("Unauthorized");
      }

      const data = await res.json();
      setHistory(data);
    } catch (err) {
      console.error("History fetch failed");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  // 🔽 PDF DOWNLOAD
  const downloadPDF = (id) => {
    const url = `http://127.0.0.1:8000/api/report/${id}/`;
    window.open(url, "_blank");
  };

  const chartData =
    result &&
    result.type_distribution && {
      labels: Object.keys(result.type_distribution),
      datasets: [
        {
          label: "Equipment Count",
          data: Object.values(result.type_distribution),
          backgroundColor: "rgba(54, 162, 235, 0.7)",
        },
      ],
    };

  return (
    <div className="app-container">
      <h1 className="title">Chemical Equipment Parameter Visualizer</h1>

      {/* Upload Section */}
      <div className="card">
        <h3>Upload CSV</h3>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <p className="hint">Upload a CSV containing equipment parameters</p>
        <button onClick={handleUpload}>Upload CSV</button>
        {error && <p className="error">{error}</p>}
      </div>

      {result && (
        <>
          {/* Chart */}
          <div className="card">
            <h3>Equipment Type Distribution</h3>
            <Bar
              data={chartData}
              options={{
                responsive: true,
                plugins: {
                  legend: { position: "top" },
                  title: {
                    display: true,
                    text: "Equipment Type Distribution",
                  },
                },
              }}
            />
          </div>

          {/* Latest Summary */}
          <div className="card">
            <h3>Latest Summary</h3>
            <pre>{JSON.stringify(result, null, 2)}</pre>

            {history.length > 0 && (
              <button
                className="toggle-btn"
                onClick={() => downloadPDF(history[0].id)}
              >
                Download PDF
              </button>
            )}
          </div>

          {/* Upload History */}
          <div className="card">
            <div className="history-header">
              <h3>Upload History</h3>
              <button
                className="toggle-btn"
                onClick={() => setShowHistory(!showHistory)}
              >
                {showHistory ? "Hide History" : "Show History"}
              </button>
            </div>

            {showHistory && (
              <div className="history-row">
                {history.map((item, index) => (
                  <div className="history-card" key={index}>
                    <strong>
                      {new Date(item.uploaded_at).toLocaleString()}
                    </strong>

                    <pre>{JSON.stringify(item.summary, null, 2)}</pre>

                    <button
                      className="toggle-btn"
                      onClick={() => downloadPDF(item.id)}
                    >
                      Download PDF
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default App;








