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
        Citizen["👤 Citizen<br/>Web Browser or Mobile"]
        Admin["👮 Municipal Administrator<br/>Admin Management Console"]
        Worker["👷 Field Worker<br/>Field Task Execution Portal"]
    end

    subgraph ClientLayer["Frontend Presentation Layer"]
        UI_Citizen["Citizen UI<br/>Jinja2, CSS3, Leaflet Map"]
        UI_Admin["Admin Analytics UI<br/>Chart.js, DataTables"]
        UI_Worker["Worker UI<br/>Task Board, Camera Upload"]
    end

    subgraph Gateway["Application Gateway & Routing"]
        WebGateway["Flask WSGI Application Engine<br/>Port 5000"]
        SecurityMW["Security Middleware<br/>RBAC, Session, HTTP Headers"]
    end

    subgraph ServiceLayer["Service & Business Logic Tier"]
        AuthSvc["AuthService<br/>PBKDF2 Password Hashing"]
        CompSvc["ComplaintService<br/>State Machine & Workflows"]
        DupSvc["DuplicateDetectionService<br/>SBERT + TF-IDF + Haversine"]
        AnalytSvc["AnalyticsService<br/>Chart Metrics & CSV Generator"]
        NotifSvc["NotificationService<br/>In-App & SMTP Engine"]
        ImgSvc["ImageService<br/>UUID Validation & Resizing"]
    end

    subgraph DataLayer["Persistence & Machine Learning Models"]
        OracleDB[("Oracle Database XE or Free<br/>FREEPDB1 Relational DB")]
        FileSystem[("Static Media Storage<br/>Uploads and Resolution Proofs")]
        MLModels["Pretrained SBERT Model<br/>all-MiniLM-L6-v2"]
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
        number USER_ID PK "Identity"
        string FULL_NAME "Full Name"
        string EMAIL UK "Unique Email"
        string USER_PASSWORD "Hashed Password"
        string PHONE_NUMBER "Contact Number"
        string ROLE "Citizen Admin or Worker"
        timestamp CREATED_AT "Registration Time"
    }

    ISSUE_CATEGORIES {
        number CATEGORY_ID PK "Category ID 6 to 10"
        string CATEGORY_NAME UK "Unique Title"
        string DESCRIPTION "Category Details"
        timestamp CREATED_AT "Creation Time"
    }

    COMPLAINTS {
        number COMPLAINT_ID PK "Identity"
        number USER_ID FK "Reporting Citizen"
        number CATEGORY_ID FK "Issue Category"
        string TITLE "Issue Headline"
        string DESCRIPTION "Detailed Narrative"
        string SEVERITY "Low Med High Critical"
        string LOCATION "Street Address"
        number LATITUDE "GPS Latitude"
        number LONGITUDE "GPS Longitude"
        string IMAGE_PATH "Initial Photo Path"
        string STATUS "Current State"
        string PRIORITY "Low Med High Critical"
        timestamp CREATED_AT "Submission Time"
        timestamp UPDATED_AT "Last Modified"
        number ASSIGNED_TO FK "Assigned Field Worker"
        string RESOLUTION_PROOF "After Photo Path"
        timestamp RESOLVED_AT "Resolution Time"
    }

    STATUS_HISTORY {
        number HISTORY_ID PK "Identity"
        number COMPLAINT_ID FK "Complaint Reference"
        string OLD_STATUS "Previous State"
        string NEW_STATUS "New State"
        number CHANGED_BY FK "Actor User ID"
        timestamp CHANGED_AT "Transition Time"
        string REMARKS "Audit Notes"
    }

    COMPLAINT_IMAGES {
        number IMAGE_ID PK "Identity"
        number COMPLAINT_ID FK "Complaint Reference"
        string IMAGE_PATH "Filesystem Path"
        string IMAGE_TYPE "COMPLAINT or RESOLUTION"
        timestamp UPLOADED_AT "Upload Time"
    }

    NOTIFICATIONS {
        number NOTIFICATION_ID PK "Identity"
        number USER_ID FK "Recipient User ID"
        number COMPLAINT_ID FK "Complaint Reference"
        string MESSAGE "Notification Content"
        number IS_READ "0 Unread 1 Read"
        timestamp CREATED_AT "Creation Time"
    }

    COMPLAINT_UPVOTES {
        number UPVOTE_ID PK "Identity"
        number COMPLAINT_ID FK "Complaint Reference"
        number USER_ID FK "Voter User ID"
        timestamp CREATED_AT "Upvote Time"
    }

    COMPLAINT_FEEDBACK {
        number FEEDBACK_ID PK "Identity"
        number COMPLAINT_ID FK "Unique per Complaint"
        number USER_ID FK "Citizen User ID"
        number RATING "1 to 5 Stars"
        string COMMENTS "Feedback Text"
        timestamp CREATED_AT "Review Time"
    }
```

---

## 6. Complaint Lifecycle & Finite State Machine (FSM)

The grievance workflow enforces strict state progression rules. Arbitrary status jumps are prevented both in the Service layer and via database constraints.

```mermaid
stateDiagram-v2
    [*] --> Pending : Citizen lodges grievance
    Pending --> Verified : Admin verifies validity
    Pending --> Rejected : Admin rejects spam or invalid
    Verified --> Assigned : Admin assigns field worker
    Assigned --> In_Progress : Worker starts field operation
    In_Progress --> Resolved : Worker uploads photo proof
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
        GPS["GPS Coordinates Lat and Lon"]
    end

    subgraph Step1["1. Database Candidate Retrieval"]
        CandidateFilter["Query Open Complaints in Same Category<br/>STATUS not in Resolved, Rejected"]
    end

    subgraph Step2["2. Geospatial Haversine Filter"]
        CalcDist["Calculate Spherical Distance<br/>via Haversine Equation"]
        ProximityCheck{"Distance <= 100 meters?"}
        SpatialScore["Compute Spatial Similarity Score<br/>1.0 - distance / 100.0"]
        SpatialPass["Spatial Proximity Flag = True"]
        SpatialFail["Spatial Proximity Flag = False<br/>No Location Overlap"]
    end

    subgraph Step3["3. Hybrid NLP Semantic Engine"]
        CheckSBERT{"Is Sentence-Transformers<br/>SBERT Available?"}
        SBERT_Flow["Dense Semantic Embeddings<br/>Model: all-MiniLM-L6-v2<br/>384-dimensional dense vectors"]
        TFIDF_Flow["Sparse TF-IDF Vectorizer<br/>plus Cosine Similarity Fallback"]
        TextScore["Compute Semantic Similarity Score 0.0 to 1.0"]
    end

    subgraph Step4["4. Composite Scoring & Decision"]
        CompositeCalc["Composite Score Formula<br/>Score = 0.6 Semantic + 0.4 Spatial"]
        DuplicateDecision{"Composite Score >= 0.65<br/>or High Text and Spatial Match?"}
        AlertUser["Return AJAX Duplicate Alert HTTP 200<br/>Warn Citizen with Existing Issue Details"]
        Proceed["Allow New Grievance Submission"]
    end

    Title --> CandidateFilter
    Desc --> CandidateFilter
    Cat --> CandidateFilter
    GPS --> CandidateFilter

    CandidateFilter --> CalcDist
    CalcDist --> ProximityCheck
    ProximityCheck -- Yes --> SpatialScore
    SpatialScore --> SpatialPass
    ProximityCheck -- No --> SpatialFail

    Title --> CheckSBERT
    Desc --> CheckSBERT
    CheckSBERT -- Yes --> SBERT_Flow
    SBERT_Flow --> TextScore
    CheckSBERT -- No --> TFIDF_Flow
    TFIDF_Flow --> TextScore

    SpatialPass --> CompositeCalc
    SpatialFail --> CompositeCalc
    TextScore --> CompositeCalc

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
    Request["Incoming HTTP Request"] --> SecHeaders["HTTP Security Headers Filter<br/>nosniff, SAMEORIGIN, XSS-Protection"]
    
    SecHeaders --> SessionCheck{"Session Authenticated?<br/>session user_id present"}
    
    SessionCheck -- No --> PublicRoute{"Is Route Public?<br/>public, about, auth"}
    PublicRoute -- Yes --> ServePublic["Serve Public Response"]
    PublicRoute -- No --> RedirectLogin["Redirect to Login Portal"]

    SessionCheck -- Yes --> RoleDecorator{"Role Verification<br/>role_required Decorator"}
    
    RoleDecorator -- "Role == Citizen" --> CitizenGate{"Target Route in Citizen or API"}
    RoleDecorator -- "Role == Admin" --> AdminGate{"Target Route in Admin or API"}
    RoleDecorator -- "Role == Worker" --> WorkerGate{"Target Route in Worker or API"}

    CitizenGate -- Authorized --> Controller["Execute Blueprint Controller"]
    AdminGate -- Authorized --> Controller
    WorkerGate -- Authorized --> Controller

    CitizenGate -- Forbidden --> Abort403["Abort 403 Forbidden<br/>Unauthorized Role Access"]
    AdminGate -- Forbidden --> Abort403
    WorkerGate -- Forbidden --> Abort403

    Controller --> ParamSQL["Parameterized SQL Execution<br/>Named bind parameters"]
    ParamSQL --> Oracle["Oracle Database FREEPDB1"]
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
        Desktop["Desktop Browsers<br/>Chrome, Edge, Firefox"]
        Mobile["Mobile Smart Devices<br/>Android, iOS Web"]
    end

    subgraph ServerTier["Application Host Localhost or VM"]
        subgraph WebServer["WSGI Web Server"]
            Flask["Flask Application Instance<br/>Python 3.10+, oracledb, Jinja2"]
        end

        subgraph Storage["File Storage"]
            UploadsComplaints["static/uploads/complaints/"]
            UploadsProofs["static/uploads/resolution_proofs/"]
        end

        subgraph MLWorker["ML Computational Engine"]
            PyTorch["PyTorch and Transformers<br/>CPU Inference Engine"]
        end
    end

    subgraph DatabaseTier["Database Host"]
        OracleService["Oracle Database XE or Free<br/>Service: FREEPDB1 Port: 1521<br/>Dedicated Relational Engine"]
    end

    Clients --> Flask
    Flask --> Storage
    Flask --> MLWorker
    Flask --> OracleService
```

---

## 📝 Document Summary & Verification

This architecture document provides a complete technical specification for **CivicPulse**. Every architectural diagram, entity relationship, state machine, and sequence matches the actual running implementation in the codebase and has been verified by the automated test suite (`tests/test_civicpulse.py`).

