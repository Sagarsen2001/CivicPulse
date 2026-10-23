# 🏛️ CivicPulse — Comprehensive System Architecture Document

> **Project:** CivicPulse — Smart Citizen Grievance Management System  
> **Course / Degree:** Master of Computer Applications (MCA) — Final / Placement Project  
> **Institution:** National Institute of Technology Warangal  
> **Author:** Sagar Sen Sethi  
> **Architecture Pattern:** Multi-Tier Layered Architecture with Service-Repository Separation and Hybrid AI/ML Geospatial Pipeline  
> **Primary Technologies:** Python 3, Flask, Oracle Database XE/Free (`FREEPDB1`), Sentence-Transformers (SBERT), scikit-learn, Leaflet.js, Chart.js  

---

## 📑 Table of Contents
1. [Executive Summary & Architectural Paradigm](#1-executive-summary--architectural-paradigm)
2. [High-Level System Context Architecture](#2-high-level-system-context-architecture)
3. [Layered Software Architecture (Multi-Tier)](#3-layered-software-architecture-multi-tier)
4. [Component & Package Structure Mapping](#4-component--package-structure-mapping)
5. [Database Entity-Relationship (ER) Architecture](#5-database-entity-relationship-er-architecture)
6. [Complaint Lifecycle & Finite State Machine (FSM)](#6-complaint-lifecycle--finite-state-machine-fsm)
7. [AI/ML Duplicate Detection & Geospatial Pipeline](#7-aiml-duplicate-detection--geospatial-pipeline)
8. [Role-Based Access Control (RBAC) & Security Architecture](#8-role-based-access-control-rbac--security-architecture)
9. [Component Interaction & Sequence Diagrams](#9-component-interaction--sequence-diagrams)
   - 9.1 Citizen Complaint Registration & Real-time AI Duplicate Detection
   - 9.2 Administrative Verification & Field Worker Dispatch
   - 9.3 Field Worker Task Execution & Photographic Resolution
10. [Notification & Event Dispatch Architecture](#10-notification--event-dispatch-architecture)
11. [Deployment Topology & Hardware Environment](#11-deployment-topology--hardware-environment)

---

## 1. Executive Summary & Architectural Paradigm

**CivicPulse** is an enterprise-scale, citizen-centric grievance redressal platform engineered for municipal administrative bodies. The architecture follows modern software engineering principles:

- **Layered Decoupling:** Strict separation between the Presentation Layer (Jinja2, responsive CSS, client-side JS), Routing & Middleware Layer (Flask Blueprints with RBAC decorators), Service/Business Logic Layer, Data Access Models, and the Oracle Relational Database.
- **Service-Repository Design Pattern:** Route handlers delegate business rules, computational scoring, and transactional operations to specialized Service classes (`ComplaintService`, `DuplicateDetectionService`, `AnalyticsService`, `NotificationService`).
- **Hybrid AI/ML & Geospatial Engine:** Natural Language Processing (SBERT embeddings with TF-IDF fallback) coupled with spherical Haversine distance computations to detect duplicate complaints within a 100-meter radius in real-time.
- **ACID Transactional Integrity:** Leverages Oracle Database Free (`FREEPDB1`) for atomic status transitions, comprehensive foreign-key constraints, check constraints, and immutable audit logging in `STATUS_HISTORY`.
- **Defensive Production Security:** Enforces parameterized queries across 100% of SQL statements, HTTP security headers (`nosniff`, `SAMEORIGIN`, `XSS-Protection`), session cookie flags (`HttpOnly`, `SameSite=Lax`), and strict file upload validation with UUID renaming.

---

## 2. High-Level System Context Architecture

The following diagram illustrates the interactions between user roles, external interfaces, computational modules, and the persistence tier:

```mermaid
flowchart TD
    subgraph Actors["User Personas"]
        Citizen["👤 Citizen\n(Web Browser / Mobile)"]
        Admin["👮 Municipal Administrator\n(Admin Console)"]
        Worker["👷 Field Worker\n(Mobile / Tablet View)"]
    end

    subgraph ClientLayer["Frontend Presentation Layer"]
        UI_Citizen["Citizen UI\n(Jinja2 / CSS3 / Leaflet Map)"]
        UI_Admin["Admin Analytics UI\n(Chart.js / DataTables)"]
        UI_Worker["Worker UI\n(Task Board / Camera Upload)"]
    end

    subgraph Gateway["Application Gateway & Routing"]
        WebGateway["Flask WSGI Application Engine\n(Port 5000)"]
        SecurityMW["Security Middleware\n(RBAC / Session / HTTP Headers)"]
    end

    subgraph ServiceLayer["Service & Business Logic Tier"]
        AuthSvc["AuthService\n(PBKDF2 Password Hashing)"]
        CompSvc["ComplaintService\n(State Machine & Workflows)"]
        DupSvc["DuplicateDetectionService\n(SBERT + TF-IDF + Haversine)"]
        AnalytSvc["AnalyticsService\n(Chart Metrics & CSV Generator)"]
        NotifSvc["NotificationService\n(In-App & SMTP Engine)"]
        ImgSvc["ImageService\n(UUID Validation & Resizing)"]
    end

    subgraph DataLayer["Persistence & Machine Learning Models"]
        OracleDB[("Oracle Database XE/Free\n(FREEPDB1:1521)\n8 Relational Tables")]
        FileSystem[("Static Media Storage\n(Uploads / Resolution Proofs)")]
        MLModels["Pretrained SBERT Model\n(all-MiniLM-L6-v2)"]
    end

    Citizen --> UI_Citizen
    Admin --> UI_Admin
    Worker --> UI_Worker

    UI_Citizen --> WebGateway
    UI_Admin --> WebGateway
    UI_Worker --> WebGateway

    WebGateway --> SecurityMW
    SecurityMW --> AuthSvc
    SecurityMW --> CompSvc
    SecurityMW --> AnalytSvc

    CompSvc --> DupSvc
    CompSvc --> NotifSvc
    CompSvc --> ImgSvc

    DupSvc --> MLModels
    CompSvc --> OracleDB
    AuthSvc --> OracleDB
    AnalytSvc --> OracleDB
    NotifSvc --> OracleDB
    ImgSvc --> FileSystem
```

---

## 3. Layered Software Architecture (Multi-Tier)

CivicPulse is structured across five discrete vertical layers:

```mermaid
flowchart TD
    subgraph PresentationTier["1. Presentation Tier (Client / Browser)"]
        P1["HTML5 / Jinja2 Server-Side Rendered Templates"]
        P2["Modular CSS3 Layouts (main.css, citizen.css, admin.css, worker.css)"]
        P3["Interactive JavaScript (AJAX Duplicate Check, Leaflet.js Maps, Chart.js)"]
    end

    subgraph RoutingTier["2. Routing & Middleware Tier (Flask Blueprints)"]
        R1["public_bp: Landing page, About, Categories, How It Works"]
        R2["auth_bp: Login, Registration, Logout"]
        R3["citizen_bp: Report Issue, My Complaints, Detail, Upvote, Feedback"]
        R4["admin_bp: Dashboard, Workflow Verification, Assignment, Map, Export"]
        R5["worker_bp: Worker Tasks, Status Progression, Resolution Proof"]
        R6["api_bp: AJAX Duplicate Detection API, GeoJSON Endpoints"]
        R7["Security Middleware: RBAC Decorators, Session Validator, Security Headers"]
    end

    subgraph BusinessTier["3. Business Logic & Service Tier"]
        B1["ComplaintService: State management, category validation, workflow progression"]
        B2["DuplicateDetectionService: SBERT embeddings, TF-IDF cosine matching, Haversine GPS"]
        B3["AnalyticsService: SQL aggregation, department breakdown, SLA metrics, CSV export"]
        B4["NotificationService: In-app notification creation, SMTP email delivery"]
        B5["ImageService: Whitelist extension check, secure UUID naming, directory management"]
        B6["ValidationService: Regex-based email/phone/password complexity verification"]
    end

    subgraph ModelTier["4. Data Access Tier (Models)"]
        M1["UserModel: User retrieval, credential validation, worker rosters"]
        M2["ComplaintModel: Multi-table joined queries, filtering, search, pagination"]
        M3["ComplaintImageModel: Multi-image record management"]
        M4["StatusHistoryModel: Immutable audit timeline records"]
        M5["Connection: Database connection pooling and cursor lifecycle"]
    end

    subgraph PersistenceTier["5. Persistence & Storage Tier"]
        D1[("Oracle Database Free / FREEPDB1 (Tables, Indexes, Sequences, Foreign Keys)")]
        D2[("Local Storage: static/uploads/complaints/ & static/uploads/resolution_proofs/")]
    end

    PresentationTier --> RoutingTier
    RoutingTier --> BusinessTier
    BusinessTier --> ModelTier
    ModelTier --> PersistenceTier
```

---

## 4. Component & Package Structure Mapping

The physical file layout directly mirrors the architectural layers:

```text
civicpulse/
│
├── app.py                         # Application Entry Point & Blueprint Registration
├── config.py                      # Centralized Configuration & Environment Variables
│
├── database/                      # Database Access & Schema Migrations
│   ├── connection.py              # Oracle oracledb connection manager & pool
│   ├── schema.sql                 # Base schema definitions
│   ├── run_migrations.py          # Automated migration runner
│   └── migrations/                # Versioned SQL migration files (001, 002, 003)
│
├── routes/                        # Routing Tier (Flask Blueprints)
│   ├── public_routes.py           # Public landing and information routes
│   ├── auth_routes.py             # User authentication & session routes
│   ├── citizen_routes.py          # Citizen reporting, tracking, voting routes
│   ├── admin_routes.py            # Administrative management, assign, export
│   ├── worker_routes.py           # Field worker task lifecycle routes
│   └── api_routes.py              # Asynchronous AJAX endpoints (duplicate check)
│
├── services/                      # Business Logic & Computational Tier
│   ├── auth_service.py            # Registration, login logic, password hashing
│   ├── complaint_service.py       # Workflow progression & business rules
│   ├── duplicate_service.py       # Hybrid SBERT + TF-IDF + Haversine Engine
│   ├── analytics_service.py       # Analytical queries & CSV generation
│   ├── notification_service.py    # In-app notifications & SMTP mailer
│   ├── image_service.py           # Secure file validation & filesystem storage
│   └── validation_service.py      # Form data and schema validator
│
├── models/                        # Data Access Object (DAO) Model Tier
│   ├── user_model.py              # User entity queries
│   ├── complaint_model.py         # Complaint data access and joins
│   ├── complaint_image_model.py   # Image association queries
│   └── status_history_model.py    # Audit history persistence
│
├── utils/                         # Reusable Cross-Cutting Utilities
│   ├── decorators.py              # @login_required, @role_required, @admin_required
│   ├── distance_utils.py          # Haversine mathematical distance formula
│   └── file_utils.py              # Extension validation & UUID generation
│
├── templates/                     # Presentation Tier (Jinja2 Templates)
│   ├── base.html                  # Master layout with responsive navbar & alerts
│   ├── public/                    # Home, About, Categories, How It Works
│   ├── auth/                      # Login and Registration forms
│   ├── citizen/                   # Citizen dashboard, report form, details
│   ├── admin/                     # Admin dashboard, complaint queue, workers, map
│   ├── worker/                    # Worker dashboard, task execution view
│   └── errors/                    # 400, 403, 404, 500 custom error pages
│
├── static/                        # Static Assets (CSS, JS, Uploads)
│   ├── css/                       # Modular stylesheets (main, citizen, admin, worker)
│   ├── js/                        # Client-side scripts (duplicate_check, admin_dashboard)
│   └── uploads/                   # Uploaded citizen photos & resolution proofs
│
├── tests/                         # Test Suite
│   └── test_civicpulse.py         # 16 Automated Integration & Unit Tests
│
└── docs/                          # Architectural & Design Documentation
    ├── system_architecture.md     # This comprehensive document
    ├── database_design.md         # Detailed Relational Database Design
    └── project_problem_statement.md # Academic problem formulation
```

---

## 5. Database Entity-Relationship (ER) Architecture

The persistence layer is modeled with 8 normalized relational tables in Oracle Database XE/Free (`FREEPDB1`). All tables feature primary keys, foreign key constraints with referential integrity, check constraints, and performance indexes.

```mermaid
erDiagram
    USERS ||--o{ COMPLAINTS : "submits"
    USERS ||--o{ COMPLAINTS : "assigned_to (worker)"
    USERS ||--o{ STATUS_HISTORY : "changed_by"
    USERS ||--o{ NOTIFICATIONS : "receives"
    USERS ||--o{ COMPLAINT_UPVOTES : "casts"
    USERS ||--o{ COMPLAINT_FEEDBACK : "submits"

    ISSUE_CATEGORIES ||--o{ COMPLAINTS : "categorizes"

    COMPLAINTS ||--o{ STATUS_HISTORY : "tracks"
    COMPLAINTS ||--o{ COMPLAINT_IMAGES : "contains"
    COMPLAINTS ||--o{ NOTIFICATIONS : "triggers"
    COMPLAINTS ||--o{ COMPLAINT_UPVOTES : "receives"
    COMPLAINTS ||--o| COMPLAINT_FEEDBACK : "evaluated_by"

    USERS {
        NUMBER USER_ID PK "Identity"
        VARCHAR2 FULL_NAME "Not Null"
        VARCHAR2 EMAIL "Unique, Not Null"
        VARCHAR2 USER_PASSWORD "Hash, Not Null"
        VARCHAR2 PHONE_NUMBER "Nullable"
        VARCHAR2 ROLE "Citizen | Admin | Worker"
        TIMESTAMP CREATED_AT "Default Current_Timestamp"
    }

    ISSUE_CATEGORIES {
        NUMBER CATEGORY_ID PK "Identity (IDs 6-10)"
        VARCHAR2 CATEGORY_NAME "Unique, Not Null"
        VARCHAR2 DESCRIPTION "Nullable"
        TIMESTAMP CREATED_AT "Default Current_Timestamp"
    }

    COMPLAINTS {
        NUMBER COMPLAINT_ID PK "Identity"
        NUMBER USER_ID FK "Citizen reference"
        NUMBER CATEGORY_ID FK "Category reference"
        VARCHAR2 TITLE "Not Null"
        VARCHAR2 DESCRIPTION "Not Null"
        VARCHAR2 SEVERITY "Low | Medium | High | Critical"
        VARCHAR2 LOCATION "Not Null"
        NUMBER LATITUDE "GPS Float (10,7)"
        NUMBER LONGITUDE "GPS Float (10,7)"
        VARCHAR2 IMAGE_PATH "Initial photo path"
        VARCHAR2 STATUS "Pending|Verified|Assigned|In Progress|Resolved|Rejected"
        VARCHAR2 PRIORITY "Low | Medium | High | Critical"
        TIMESTAMP CREATED_AT "Default Current_Timestamp"
        TIMESTAMP UPDATED_AT "Last modified"
        NUMBER ASSIGNED_TO FK "Worker reference"
        VARCHAR2 RESOLUTION_PROOF "After photo path"
        TIMESTAMP RESOLVED_AT "Resolution timestamp"
    }

    STATUS_HISTORY {
        NUMBER HISTORY_ID PK "Identity"
        NUMBER COMPLAINT_ID FK "Complaint reference"
        VARCHAR2 OLD_STATUS "Previous status"
        VARCHAR2 NEW_STATUS "New status"
        NUMBER CHANGED_BY FK "User reference"
        TIMESTAMP CHANGED_AT "Default Current_Timestamp"
        VARCHAR2 REMARKS "Transition audit notes"
    }

    COMPLAINT_IMAGES {
        NUMBER IMAGE_ID PK "Identity"
        NUMBER COMPLAINT_ID FK "Complaint reference"
        VARCHAR2 IMAGE_PATH "Filesystem relative path"
        VARCHAR2 IMAGE_TYPE "COMPLAINT | RESOLUTION"
        TIMESTAMP UPLOADED_AT "Default Current_Timestamp"
    }

    NOTIFICATIONS {
        NUMBER NOTIFICATION_ID PK "Identity"
        NUMBER USER_ID FK "Recipient user"
        NUMBER COMPLAINT_ID FK "Linked complaint"
        VARCHAR2 MESSAGE "Text content"
        NUMBER IS_READ "0 = Unread, 1 = Read"
        TIMESTAMP CREATED_AT "Default Current_Timestamp"
    }

    COMPLAINT_UPVOTES {
        NUMBER UPVOTE_ID PK "Identity"
        NUMBER COMPLAINT_ID FK "Complaint reference"
        NUMBER USER_ID FK "User reference"
        TIMESTAMP CREATED_AT "Default Current_Timestamp"
    }

    COMPLAINT_FEEDBACK {
        NUMBER FEEDBACK_ID PK "Identity"
        NUMBER COMPLAINT_ID FK "Unique per complaint"
        NUMBER USER_ID FK "Citizen reference"
        NUMBER RATING "1 to 5 Stars"
        VARCHAR2 COMMENTS "Feedback text"
        TIMESTAMP CREATED_AT "Default Current_Timestamp"
    }
```

---

## 6. Complaint Lifecycle & Finite State Machine (FSM)

The grievance workflow enforces strict state progression rules. Arbitrary status jumps are prevented both in the Service layer and via database constraints.

```mermaid
stateDiagram-v2
    [*] --> Pending : Citizen submits complaint (Initial state)

    state "Pending" as Pending {
        description: Awaiting administrative review
    }

    Pending --> Verified : Admin approves complaint\n(Valid issue confirmed)
    Pending --> Rejected : Admin rejects complaint\n(Spam, invalid, or outside jurisdiction)

    state "Verified" as Verified {
        description: Validated issue ready for assignment
    }

    Verified --> Assigned : Admin assigns to Field Worker\n(ASSIGNED_TO updated, Worker notified)

    state "Assigned" as Assigned {
        description: Dispatched to worker task queue
    }

    Assigned --> In_Progress : Worker starts field operation\n(Status updated via Worker Portal)

    state "In_Progress" as In_Progress {
        description: Physical maintenance underway
    }

    In_Progress --> Resolved : Worker uploads photo proof & marks complete\n(RESOLUTION_PROOF saved, Citizen notified)

    state "Resolved" as Resolved {
        description: Problem solved, Citizen can rate & upvote
    }

    state "Rejected" as Rejected {
        description: Grievance dismissed with administrative reason
    }

    Resolved --> [*]
    Rejected --> [*]
```

### State Transition Validation Matrix

| Current Status | Next Allowed Status | Permitted Actor | Mandatory Requirements |
|---|---|---|---|
| **None** | `Pending` | Citizen | Valid title, description, category, and location. |
| **Pending** | `Verified` | Admin | Administrative review. |
| **Pending** | `Rejected` | Admin | Rejection reason comment logged to `STATUS_HISTORY`. |
| **Verified** | `Assigned` | Admin | Selection of active user with `ROLE = 'Worker'`. |
| **Assigned** | `In Progress` | Assigned Worker | Worker identity check (`session['user_id'] == ASSIGNED_TO`). |
| **In Progress** | `Resolved` | Assigned Worker | Mandatory upload of Photographic Resolution Proof. |

---

## 7. AI/ML Duplicate Detection & Geospatial Pipeline

To eliminate redundant civic complaints (e.g., multiple citizens reporting the same pothole on the same street), CivicPulse implements an automated duplicate detection pipeline combining **Natural Language Processing (NLP)** and **Geospatial Proximity Calculation**.

```mermaid
flowchart TD
    subgraph Input["Citizen Form Input"]
        Title["Complaint Title"]
        Desc["Complaint Description"]
        Cat["Category ID"]
        GPS["GPS Coordinates (Lat, Lon)"]
    end

    subgraph Step1["1. Database Candidate Retrieval"]
        CandidateFilter["Query Open Complaints in Same Category\n(STATUS != 'Resolved' AND STATUS != 'Rejected')"]
    end

    subgraph Step2["2. Geospatial Haversine Filter"]
        CalcDist["Calculate Spherical Distance\nvia Haversine Equation"]
        ProximityCheck{"Distance <= 100 meters?"}
        SpatialScore["Compute Spatial Similarity Score\n(1.0 - distance / 100.0)"]
        SpatialPass["Spatial Proximity Flag = True"]
        SpatialFail["Spatial Proximity Flag = False\n(No Location Overlap)"]
    end

    subgraph Step3["3. Hybrid NLP Semantic Engine"]
        CheckSBERT{"Is Sentence-Transformers\n(SBERT) Available?"}
        SBERT_Flow["Dense Semantic Embeddings\nModel: all-MiniLM-L6-v2\n384-dimensional dense vectors"]
        TFIDF_Flow["Sparse TF-IDF Vectorizer\n+ Cosine Similarity Fallback\n(scikit-learn)"]
        TextScore["Compute Semantic Similarity Score [0.0, 1.0]"]
    end

    subgraph Step4["4. Composite Scoring & Decision"]
        CompositeCalc["Composite Score Formula:\nScore = (0.6 * SemanticScore) + (0.4 * SpatialScore)"]
        DuplicateDecision{"Composite Score >= 0.65\nOR (Semantic >= 0.75 AND Spatial = True)?"}
        AlertUser["Return AJAX Duplicate Alert (HTTP 200)\nWarn Citizen with Existing Complaint ID & Title"]
        Proceed["Allow New Submission"]
    end

    Title & Desc & Cat & GPS --> CandidateFilter
    CandidateFilter --> CalcDist
    CalcDist --> ProximityCheck
    ProximityCheck -- Yes --> SpatialScore --> SpatialPass
    ProximityCheck -- No --> SpatialFail

    Title & Desc --> CheckSBERT
    CheckSBERT -- Yes --> SBERT_Flow --> TextScore
    CheckSBERT -- No --> TFIDF_Flow --> TextScore

    SpatialPass & TextScore --> CompositeCalc
    SpatialFail & TextScore --> CompositeCalc

    CompositeCalc --> DuplicateDecision
    DuplicateDecision -- Yes --> AlertUser
    DuplicateDecision -- No --> Proceed
```

### Mathematical Haversine Distance Formula

The great-circle distance between two GPS coordinates $(\phi_1, \lambda_1)$ and $(\phi_2, \lambda_2)$ on Earth (mean radius $R = 6371\text{ km}$) is computed as:

$$\Delta\phi = \phi_2 - \phi_1, \quad \Delta\lambda = \lambda_2 - \lambda_1$$

$$a = \sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)$$

$$c = 2 \cdot \operatorname{atan2}\left(\sqrt{a}, \sqrt{1-a}\right)$$

$$d = R \cdot c \quad (\text{in meters: } d \times 1000)$$

If $d \le 100\text{ meters}$, the issues are flagged as geographically co-located.

---

## 8. Role-Based Access Control (RBAC) & Security Architecture

CivicPulse implements multi-layered defensive security ensuring complete role isolation and vulnerability mitigation.

```mermaid
flowchart TD
    Request["Incoming HTTP Request"] --> SecHeaders["HTTP Security Headers Filter\n• X-Content-Type-Options: nosniff\n• X-Frame-Options: SAMEORIGIN\n• X-XSS-Protection: 1; mode=block"]
    
    SecHeaders --> SessionCheck{"Session Authenticated?\n(session['user_id'] present)"}
    
    SessionCheck -- No --> PublicRoute{"Is Route Public?\n(/, /about, /auth/*)"}
    PublicRoute -- Yes --> ServePublic["Serve Public Response"]
    PublicRoute -- No --> RedirectLogin["Redirect to /auth/login\n(Flash: 'Please login first')"]

    SessionCheck -- Yes --> RoleDecorator{"Role Verification\n(@role_required Decorator)"}
    
    RoleDecorator -- "Role == 'Citizen'" --> CitizenGate{"Target Route in\n/citizen/* OR /api/*?"}
    RoleDecorator -- "Role == 'Admin'" --> AdminGate{"Target Route in\n/admin/* OR /api/*?"}
    RoleDecorator -- "Role == 'Worker'" --> WorkerGate{"Target Route in\n/worker/* OR /api/*?"}

    CitizenGate -- Authorized --> Controller["Execute Blueprint Controller"]
    AdminGate -- Authorized --> Controller
    WorkerGate -- Authorized --> Controller

    CitizenGate -- Forbidden --> Abort403["Abort 403 Forbidden\n(Unauthorized Role Access)"]
    AdminGate -- Forbidden --> Abort403
    WorkerGate -- Forbidden --> Abort403

    Controller --> ParamSQL["Parameterized SQL Execution\n(:param_name named binds)"]
    ParamSQL --> Oracle["Oracle Database (FREEPDB1)"]
```

### Access Control Matrix

| Feature / Resource Endpoint | Public Guest | Citizen | Municipal Admin | Field Worker |
|---|:---:|:---:|:---:|:---:|
| Home, About, How It Works, Categories | ✅ | ✅ | ✅ | ✅ |
| Login / Register | ✅ | Redirect | Redirect | Redirect |
| Citizen Dashboard & Report Issue Form | ❌ | ✅ | ❌ | ❌ |
| View My Complaints & Detail | ❌ | ✅ (Own Only) | ❌ | ❌ |
| Upvote / Citizen Feedback Rating | ❌ | ✅ | ❌ | ❌ |
| Admin Dashboard & Analytics Charts | ❌ | ❌ | ✅ | ❌ |
| Verify / Reject Complaints | ❌ | ❌ | ✅ | ❌ |
| Assign Complaints to Workers | ❌ | ❌ | ✅ | ❌ |
| Geospatial GIS Map & CSV Export | ❌ | ❌ | ✅ | ❌ |
| Worker Task Board & Dashboard | ❌ | ❌ | ❌ | ✅ |
| Progress Task (Assigned $\rightarrow$ In Progress) | ❌ | ❌ | ❌ | ✅ (Assigned Only) |
| Upload Resolution Proof Photo | ❌ | ❌ | ❌ | ✅ (Assigned Only) |

---

## 9. Component Interaction & Sequence Diagrams

### 9.1 Citizen Complaint Registration & Real-time AI Duplicate Detection

```mermaid
sequenceDiagram
    autonumber
    actor Citizen as Citizen
    participant UI as Citizen Browser
    participant API as /api/check-duplicates
    participant DupSvc as DuplicateDetectionService
    participant C_Route as /citizen/report
    participant CompSvc as ComplaintService
    participant ImgSvc as ImageService
    participant DB as Oracle Database
    participant Notif as NotificationService

    Citizen->>UI: Types Title, Description, selects Category, clicks Map GPS
    UI->>API: AJAX POST (title, description, category_id, lat, lon)
    API->>DupSvc: check_potential_duplicates(...)
    DupSvc->>DB: Query open complaints in same category
    DB-->>DupSvc: Candidate rows
    DupSvc->>DupSvc: Compute SBERT semantic cosine + Haversine distance
    DupSvc-->>API: Duplicate result (is_duplicate: true/false, match_id)
    API-->>UI: JSON response
    alt Potential Duplicate Found
        UI->>Citizen: Renders warning alert: "Similar issue #104 already reported nearby"
    end

    Citizen->>UI: Submits Form with optional image attachment
    UI->>C_Route: POST /citizen/report (FormData)
    C_Route->>ImgSvc: validate_and_save_image(file)
    ImgSvc-->>C_Route: Sanitized relative path (UUID filename)
    C_Route->>CompSvc: create_complaint(...)
    CompSvc->>DB: INSERT INTO COMPLAINTS (STATUS='Pending')
    CompSvc->>DB: INSERT INTO STATUS_HISTORY (NEW_STATUS='Pending')
    CompSvc->>Notif: notify_complaint_submitted(user_id, complaint_id)
    Notif->>DB: INSERT INTO NOTIFICATIONS
    CompSvc-->>C_Route: Success (complaint_id)
    C_Route-->>UI: Redirect to /citizen/complaint/<id> with success flash
```

### 9.2 Administrative Verification & Field Worker Dispatch

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Municipal Admin
    participant UI as Admin Portal
    participant Route as admin_routes.py
    participant CompSvc as ComplaintService
    participant DB as Oracle Database
    participant Notif as NotificationService

    Admin->>UI: Inspects pending grievances at /admin/complaints
    UI->>Route: GET /admin/complaint/101
    Route->>DB: Fetch details, citizen info, images, status history, active workers
    DB-->>Route: Consolidated grievance record
    Route-->>UI: Renders complaint_detail.html

    Admin->>UI: Clicks "Verify Complaint"
    UI->>Route: POST /admin/complaint/101/verify
    Route->>CompSvc: verify_complaint(101, admin_id)
    CompSvc->>DB: UPDATE COMPLAINTS SET STATUS='Verified'
    CompSvc->>DB: INSERT INTO STATUS_HISTORY (OLD='Pending', NEW='Verified')
    DB-->>Route: Commit transaction

    Admin->>UI: Selects Worker #3 from dropdown and clicks "Assign Worker"
    UI->>Route: POST /admin/complaint/101/assign (worker_id=3)
    Route->>CompSvc: assign_complaint(101, worker_id=3, admin_id)
    CompSvc->>DB: UPDATE COMPLAINTS SET STATUS='Assigned', ASSIGNED_TO=3
    CompSvc->>DB: INSERT INTO STATUS_HISTORY (OLD='Verified', NEW='Assigned')
    CompSvc->>Notif: notify_worker_assigned(worker_id=3, complaint_id=101)
    CompSvc->>Notif: notify_citizen_status_update(citizen_id, 'Assigned')
    Notif->>DB: INSERT INTO NOTIFICATIONS (Worker & Citizen records)
    Route-->>UI: Redirect with success notification
```

### 9.3 Field Worker Task Execution & Photographic Resolution

```mermaid
sequenceDiagram
    autonumber
    actor Worker as Field Worker
    participant UI as Worker Portal
    participant Route as worker_routes.py
    participant DB as Oracle Database
    participant ImgSvc as ImageService
    participant Notif as NotificationService

    Worker->>UI: Logs in & views /worker/dashboard
    UI->>Route: GET /worker/dashboard
    Route->>DB: SELECT WHERE ASSIGNED_TO = :worker_id
    DB-->>UI: Displays assigned task list sorted by Priority

    Worker->>UI: Clicks "Start Work"
    UI->>Route: POST /worker/complaint/101/update-status (new_status='In Progress')
    Route->>DB: UPDATE COMPLAINTS SET STATUS='In Progress'
    Route->>DB: INSERT INTO STATUS_HISTORY (OLD='Assigned', NEW='In Progress')
    DB-->>UI: Status updated to 'In Progress'

    Note over Worker, UI: Worker completes physical repair on site

    Worker->>UI: Captures & uploads after-repair photo, clicks "Resolve Issue"
    UI->>Route: POST /worker/complaint/101/upload-proof (Image file + Remarks)
    Route->>ImgSvc: validate_and_save_resolution_proof(file)
    ImgSvc-->>Route: Saved path (static/uploads/resolution_proofs/proof_uuid.jpg)
    Route->>DB: UPDATE COMPLAINTS SET STATUS='Resolved', RESOLUTION_PROOF=:path, RESOLVED_AT=CURRENT_TIMESTAMP
    Route->>DB: INSERT INTO COMPLAINT_IMAGES (IMAGE_TYPE='RESOLUTION')
    Route->>DB: INSERT INTO STATUS_HISTORY (OLD='In Progress', NEW='Resolved')
    Route->>Notif: notify_citizen_resolved(citizen_id, complaint_id=101)
    Notif->>DB: INSERT INTO NOTIFICATIONS
    Route-->>UI: Redirect to dashboard (Task completed)
```

---

## 10. Notification & Event Dispatch Architecture

The notification subsystem employs a dual-channel design: an immediate synchronous database notification and a decoupled SMTP mail dispatch engine with graceful error handling.

```mermaid
flowchart TD
    Trigger["System Event Triggered\n(e.g., Complaint Submitted, Assigned, Resolved)"] --> NotifDispatcher["NotificationService.dispatch_event()"]

    subgraph Channel1["Channel 1: Guaranteed In-App Notification"]
        DB_Insert["INSERT INTO NOTIFICATIONS\n(USER_ID, COMPLAINT_ID, MESSAGE, IS_READ=0)"]
        BadgeUpdate["Navbar Notification Counter Increments"]
        DB_Insert --> BadgeUpdate
    end

    subgraph Channel2["Channel 2: Outbound Email Notification (SMTP)"]
        CheckSMTP{"Is SMTP Configured\nin Environment?\n(MAIL_SERVER, MAIL_USERNAME)"}
        SendMail["Construct MIME Email & Send via SMTP SSL/TLS"]
        FallbackLog["Graceful Fallback:\nLog notification message to console\n(Zero impact on user request)"]
        
        CheckSMTP -- Yes --> SendMail
        CheckSMTP -- No --> FallbackLog
        SendMail -- "SMTP Exception / Timeout" --> FallbackLog
    end

    NotifDispatcher --> Channel1
    NotifDispatcher --> Channel2
```

---

## 11. Deployment Topology & Hardware Environment

CivicPulse is optimized for deployment on standalone server instances or cloud virtual machines (Linux/Windows).

```mermaid
flowchart LR
    subgraph Clients["Client Tier"]
        Desktop["Desktop Browsers\n(Chrome, Edge, Firefox)"]
        Mobile["Mobile Smart Devices\n(Android / iOS Web)"]
    end

    subgraph ServerTier["Application Host (Localhost / VM)"]
        subgraph WebServer["WSGI Web Server"]
            Flask["Flask Application Instance\n(Python 3.10+, oracledb, Jinja2)"]
        end

        subgraph Storage["File Storage"]
            UploadsComplaints["/static/uploads/complaints/"]
            UploadsProofs["/static/uploads/resolution_proofs/"]
        end

        subgraph MLWorker["ML Computational Engine"]
            PyTorch["PyTorch / Transformers\n(CPU Inference Engine)"]
        end
    end

    subgraph DatabaseTier["Database Host"]
        OracleService["Oracle Database XE / Free\nService: FREEPDB1\nPort: 1521\nDedicated Relational Engine"]
    end

    Clients -->|HTTP / HTTPS Port 5000| Flask
    Flask -->|File I/O| Storage
    Flask -->|In-Process Vectorization| MLWorker
    Flask -->|TCP/IP SQL Net Connections| OracleService
```

---

## 📝 Document Summary & Verification

This architecture document provides a complete technical specification for **CivicPulse**. Every architectural diagram, entity relationship, state machine, and sequence matches the actual running implementation in the codebase and has been verified by the automated test suite (`tests/test_civicpulse.py`).

