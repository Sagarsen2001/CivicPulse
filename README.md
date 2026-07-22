# 🚀 CivicPulse

> **An AI-Powered Smart Civic Complaint Management System** built using **Flask** and **Oracle Database** to streamline complaint registration, tracking, assignment, and resolution.

---

## 📌 Overview

CivicPulse is a web-based platform that enables citizens to report civic issues such as road damage, garbage accumulation, water leakage, and streetlight failures. The system allows government departments to efficiently manage complaints, assign workers, monitor progress, and analyze complaint trends through an interactive dashboard.

---

## ✨ Key Features

### 👤 Citizen Module
- Secure User Registration & Login
- Submit Civic Complaints
- Upload Complaint Images
- Track Complaint Status
- View Complaint History
- Provide Feedback After Resolution

### 🛠️ Administration Module
- Admin Authentication
- Department Management
- Worker Management
- Complaint Assignment
- Complaint Priority Management
- Complaint Status Updates
- Dashboard & Analytics

### 📊 Analytics
- Complaint Statistics
- Department-wise Reports
- Complaint Status Distribution
- Priority-wise Analysis
- Resolution Tracking

---

## 🏗️ Project Architecture

```text
Citizen
    │
    ▼
Flask Web Application
    │
    ├── Authentication
    ├── Complaint Management
    ├── Department Management
    ├── Worker Assignment
    ├── Analytics Dashboard
    │
    ▼
Oracle Database
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| Database | Oracle Database |
| Templates | Jinja2 |
| Version Control | Git, GitHub |

---

## 📂 Project Structure

```text
CivicPulse/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
├── routes/
├── services/
├── models/
├── templates/
├── static/
├── docs/
└── tests/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/CivicPulse.git
```

```bash
cd CivicPulse
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Database

Update Oracle Database credentials inside `config.py`.

---

### Run Application

```bash
python app.py
```

---

## 🌐 Open in Browser

```
http://127.0.0.1:5000
```

---

## 🚧 Current Development

The project is actively under development.

Upcoming features include:

- AI-powered complaint categorization
- Smart complaint prioritization
- Duplicate complaint detection
- Email/SMS notifications
- Interactive analytics dashboard
- Image-based complaint verification

---

## 📸 Screenshots

> Add screenshots of:

- Home Page
- Login
- Complaint Registration
- Dashboard
- Complaint Tracking
- Admin Panel

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Sagar Sen Sethi**

MCA • National Institute of Technology Warangal

GitHub: https://github.com/Sagarsen2001