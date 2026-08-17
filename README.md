# 🚀 CivicPulse

> **Smart Civic Complaint Management System** built using **Python, Flask, Oracle Database, HTML, CSS, and JavaScript**.

CivicPulse is a web-based civic complaint management platform that allows citizens to report public issues, upload supporting images, track complaint status, and monitor the progress of their complaints.

The system is designed with separate layers for presentation, routing, business logic, data access, and database management, making it easier to maintain and extend.

---

# 📌 Overview

CivicPulse addresses common problems in traditional civic complaint systems by providing a centralized digital platform for:

- Citizen registration and authentication
- Civic complaint submission
- Complaint image upload
- Location information
- Complaint categorization
- Complaint priority management
- Complaint status tracking
- Complaint history
- Status timeline
- Worker assignment
- Complaint resolution
- Feedback collection
- Administrative monitoring
- Analytics and reporting

---

# ✨ Key Features

## 👤 Citizen Module

- User Registration
- Secure Login
- Session Management
- Role-based Access
- Submit Civic Complaints
- Select Complaint Category
- Add Complaint Description
- Add Location
- Upload Complaint Images
- Set Complaint Severity
- Track Complaint Status
- View My Complaints
- Search Complaints
- Filter Complaints by Status
- View Complaint Details
- View Complaint Status Timeline
- Copy Complaint ID
- Provide Feedback After Resolution

---

## 🛠️ Admin Module

Planned / under development:

- Admin Authentication
- Department Management
- Worker Management
- Complaint Verification
- Worker Assignment
- Complaint Priority Management
- Complaint Status Management
- Complaint Monitoring
- Analytics Dashboard

---

## 👷 Worker Module

Planned / under development:

- Worker Authentication
- Assigned Complaint List
- View Complaint Details
- Update Complaint Status
- Add Resolution Remarks
- Upload Resolution Proof
- Mark Complaint as Resolved

---


# 🏗️ System Architecture

CivicPulse follows a **layered Flask architecture**.

```text
                         ┌──────────────────────┐
                         │       CITIZEN        │
                         │  Web Browser / UI    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   PRESENTATION LAYER │
                         │                      │
                         │ HTML / CSS / JS      │
                         │ Jinja2 Templates     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      ROUTING LAYER   │
                         │                      │
                         │ Flask Blueprints     │
                         │ Auth Routes          │
                         │ Citizen Routes       │
                         │ Admin Routes         │
                         │ Worker Routes        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     SERVICE LAYER    │
                         │                      │
                         │ Authentication       │
                         │ Complaint Services   │
                         │ Image Services       │
                         │ Validation           │
                         │ Business Rules       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      MODEL LAYER     │
                         │                      │
                         │ User Model           │
                         │ Complaint Model      │
                         │ Image Model          │
                         │ Status History Model │
                         │ Category Model       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    DATABASE LAYER    │
                         │                      │
                         │ Oracle Database      │
                         │                      │
                         │ USERS                │
                         │ ISSUE_CATEGORIES     │
                         │ COMPLAINTS           │
                         │ STATUS_HISTORY       │
                         └──────────────────────┘

<table> <tr> <td>
 🔄 Complaint Submission Flow

The complaint submission process follows this flow:

Citizen
   │
   │ Fill Complaint Form
   ▼
Complaint Form
   │
   ├── Title
   ├── Description
   ├── Category
   ├── Severity
   ├── Location
   └── Image
   │
   ▼
Flask Citizen Route
   │
   ▼
Validation Service
   │
   ├── Validate Form Data
   ├── Validate Image
   └── Validate Required Fields
   │
   ▼
Complaint Service
   │
   ├── Process Complaint
   ├── Save Image
   └── Calculate / Assign Priority
   │
   ▼
Complaint Model
   │
   ▼
Oracle Database
   │
   ├── COMPLAINTS
   └── STATUS_HISTORY
   │
   ▼
Complaint Created
   │
   ▼
Citizen Dashboard

</td> </tr> </table>


<table> <tr> <td>

## 🖼️ Complaint Image Upload Flow
Citizen
   │
   ▼
Select Image
   │
   ▼
Image Service
   │
   ├── Check File Extension
   ├── Validate File Type
   ├── Generate Unique Filename
   └── Save File
   │
   ▼
static/uploads/complaint_images/
   │
   ▼
Store Image Path
   │
   ▼
Oracle COMPLAINTS
The actual image file is stored in the application's upload directory, while the corresponding image path is stored in Oracle.

</td> </tr> </table>

📊 Complaint Tracking Flow
Citizen
   │
   ▼
My Complaints
   │
   ▼
Select Complaint
   │
   ▼
Complaint Details
   │
   ├── Complaint Information
   ├── Image
   ├── Current Status
   └── Status Timeline
   │
   ▼
STATUS_HISTORY
   │
   ├── Pending
   ├── Verified
   ├── Assigned
   ├── In Progress
   ├── Resolved
   └── Rejected


🗄️ Database Architecture
CivicPulse uses Oracle Database for persistent data storage.

USERS
 │
 │ USER_ID
 │
 └──────────────┐
                │
                ▼
           COMPLAINTS
                │
        ┌───────┼────────┐
        │       │        │
        ▼       ▼        ▼
   CATEGORY  STATUS   IMAGE_PATH
        │    HISTORY
        │       │
        ▼       ▼
ISSUE_CATEGORIES


Main Tables
| Table              | Purpose                                    |
| ------------------ | ------------------------------------------ |
| `USERS`            | Stores citizen, admin, and worker accounts |
| `ISSUE_CATEGORIES` | Stores civic issue categories              |
| `COMPLAINTS`       | Stores complaint information               |
| `STATUS_HISTORY`   | Stores complaint status changes            |



📂 Project Structure

CivicPulse/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   ├── connection.py
│   └── schema.sql
│
├── models/
│   ├── user_model.py
│   ├── complaint_model.py
│   ├── complaint_image_model.py
│   └── status_history_model.py
│
├── services/
│   ├── auth_service.py
│   ├── complaint_service.py
│   ├── image_service.py
│   └── validation_service.py
│
├── routes/
│   ├── public_routes.py
│   ├── auth_routes.py
│   └── citizen_routes.py
│
├── utils/
│   ├── decorators.py
│   ├── constants.py
│   └── file_utils.py
│
├── templates/
│   │
│   ├── base.html
│   │
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── citizen/
│   │   ├── dashboard.html
│   │   ├── my_complaints.html
│   │   ├── complaint_detail.html
│   │   └── report_issue.html
│   │
│   └── errors/
│
├── static/
│   │
│   ├── css/
│   │   ├── main.css
│   │   ├── home.css
│   │   ├── auth.css
│   │   ├── citizen.css
│   │   └── timeline.css
│   │
│   ├── js/
│   │   ├── main.js
│   │   ├── auth.js
│   │   ├── complaint_form.js
│   │   ├── image_preview.js
│   │   ├── citizen_dashboard.js
│   │   └── complaint_detail.js
│   │
│   └── uploads/
│       ├── complaint_images/
│       │   └── .gitkeep
│       │
│       └── resolution_proofs/
│           └── .gitkeep
│
├── docs/
│
└── tests/


🛠️ Technology Stack

| Category             | Technology              |
| -------------------- | ----------------------- |
| Programming Language | Python                  |
| Backend Framework    | Flask                   |
| Frontend             | HTML5, CSS3, JavaScript |
| Template Engine      | Jinja2                  |
| Database             | Oracle Database         |
| Database Driver      | python-oracledb         |
| Version Control      | Git                     |
| Repository           | GitHub                  |


🔐 Security

CivicPulse includes:
Session-based authentication
Role-based access control
Protected routes
Server-side validation
File type validation
Unique uploaded filenames
Environment-based configuration
.env protection through .gitignore
Sensitive database credentials are not stored in the GitHub repository.


⚙️ Installation

1. Clone Repository
git clone https://github.com/Sagarsen2001/CivicPulse.git
cd CivicPulse
2. Create Virtual Environment
python -m venv venv
Windows
venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file:

SECRET_KEY=your_secret_key
ORACLE_USER=your_oracle_username
ORACLE_PASSWORD=your_oracle_password
ORACLE_DSN=localhost:1521/FREEPDB1
Never commit the .env file to GitHub.


🗄️ Database Setup

Make sure Oracle Database is running.
Connect using SQL*Plus:
sqlplus username/password@localhost:1521/FREEPDB1
Then execute the database schema:
@database/schema.sql


▶️ Run the Application
python app.py
Open:
http://127.0.0.1:5000


🚧 Development Roadmap

✅ Completed
Project foundation
Flask application setup
Public pages
Oracle database connection
User registration
User login
Session management
Role-based access
Complaint submission
Complaint categories
Complaint severityComplaint priority
Complaint image upload
Citizen dashboard
My Complaints
Complaint details
Complaint status timeline

🔄 Upcoming

Admin dashboard
Department management
Worker management
Worker assignment
Worker dashboard
Complaint verification
Resolution proof upload
Citizen feedback
Email notifications
Analytics dashboard

🤖 Future AI Features

AI-based complaint categorization
Automatic complaint priority prediction
Duplicate complaint detection
Image-based civic issue classification
Smart complaint routing
Complaint trend prediction

📸 Screenshots

Screenshots will be added as the project progresses.
Planned screenshots:
Home Page
Registration
Login
Report Complaint
Citizen Dashboard
My Complaints
Complaint Details
Status Timeline
Admin Dashboard
Worker Dashboard
Analytics Dashboard


📜 License
This project is licensed under the MIT License.

👨‍💻 Author
Sagar Sen Sethi

MCA
National Institute of Technology Warangal

GitHub:
https://github.com/Sagarsen2001
