# Chemical Equipment Parameter Visualizer – Project Overview

## 1. Project Description

The **Chemical Equipment Parameter Visualizer** is a full-stack application designed to analyze and visualize chemical equipment data uploaded in CSV format.  
The system provides both **web-based** and **desktop-based** user interfaces that interact with a **common Django REST backend**.

The application parses equipment parameters such as **flowrate, pressure, temperature, and equipment type**, performs analytical calculations, stores recent upload history, and presents the results through **charts, summaries, and downloadable PDF reports**.

---

## 2. Objectives

- Enable users to upload chemical equipment data in CSV format
- Perform automated data analysis using Python
- Visualize results using interactive charts
- Maintain a history of recent uploads
- Support both web and desktop platforms
- Secure all sensitive operations using basic authentication
- Allow authenticated users to generate PDF reports

---

## 3. System Architecture

The system follows a **client–server architecture**:

- **Backend:** Django + Django REST Framework  
- **Frontend (Web):** React.js + Chart.js  
- **Frontend (Desktop):** PyQt5 + Matplotlib  
- **Database:** SQLite  
- **Data Processing:** Pandas  

All clients communicate with the backend using REST APIs secured via **Basic Authentication**.

---

## 4. Technology Stack

| Layer | Technology | Purpose |
|-----|-----------|--------|
| Backend | Django, Django REST Framework | API & authentication |
| Data Handling | Pandas | CSV parsing and analytics |
| Database | SQLite | Store upload history |
| Web Frontend | React.js, Chart.js | Visualization & UI |
| Desktop Frontend | PyQt5, Matplotlib | Desktop visualization |
| Authentication | HTTP Basic Auth | Secure APIs |
| PDF Generation | ReportLab | Generate reports |

---

## 5. Key Features

### 5.1 CSV Upload
- Users can upload a CSV file containing equipment details
- Supported from both **web** and **desktop** applications

### 5.2 Data Analysis
The backend calculates:
- Total number of equipment
- Average flowrate
- Average pressure
- Average temperature
- Equipment type distribution

### 5.3 Visualization
- **Web:** Bar charts using Chart.js
- **Desktop:** Bar charts using Matplotlib

### 5.4 Upload History
- Stores summaries of the **last 5 uploads**
- Accessible only to authenticated users

### 5.5 Authentication
- Uses **Django Basic Authentication**
- Protects CSV upload, history access, and PDF generation
- Both React and PyQt automatically attach credentials

### 5.6 PDF Report Generation
- Generates a downloadable PDF report for a selected upload
- Includes all computed statistics
- Available only for authenticated users

---

## 6. Workflow Overview

1. User uploads CSV file
2. Backend validates and parses data
3. Analytics are computed using Pandas
4. Summary is saved in database
5. Results are returned via API
6. Frontends visualize the data
7. User can download PDF report if authenticated

---

## 7. Sample Data

A sample CSV file (`sample_equipment_data.csv`) is provided for testing and demonstration.  
Custom CSV files with the same column structure are also supported.

---

## 8. Use Cases

- Academic demonstrations of full-stack development
- Data visualization projects
- Learning REST API integration
- Understanding authentication mechanisms
- Desktop + web hybrid application design

---

## 9. Future Enhancements

- Role-based authentication
- Export charts as images
- Support for additional file formats
- Deployment on cloud platforms
- Advanced analytics and filtering

---

## 10. Conclusion

This project demonstrates a **complete end-to-end application** integrating backend APIs, frontend visualizations, authentication, data processing, and report generation.  
It highlights best practices in **full-stack development**, **API security**, and **multi-platform support**.

---
