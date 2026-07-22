# Database Design

## Overview

The CivicPulse database is designed to manage civic complaints efficiently. It stores user information, complaint categories, and complaint details while maintaining proper relationships between tables using primary and foreign keys.

---

# Database Tables

Currently, the database contains three main tables:

1. USERS
2. ISSUE_CATEGORIES
3. COMPLAINTS

---

# 1. USERS Table

## Purpose

Stores all registered users of the system.

A user can be:

- Citizen
- Admin
- Worker

## Columns

| Column | Data Type | Description |
|---------|-----------|-------------|
| USER_ID | NUMBER | Primary Key |
| FULL_NAME | VARCHAR2(100) | User's full name |
| EMAIL | VARCHAR2(100) | Unique email address |
| PASSWORD | VARCHAR2(255) | User password |
| PHONE_NUMBER | VARCHAR2(15) | Contact number |
| ROLE | VARCHAR2(20) | Citizen/Admin/Worker |
| CREATED_AT | TIMESTAMP | Account creation time |

---

# 2. ISSUE_CATEGORIES Table

## Purpose

Stores different categories of civic issues.

Examples:

- Pothole
- Garbage
- Drainage
- Street Light
- Water Leakage

## Columns

| Column | Data Type | Description |
|---------|-----------|-------------|
| CATEGORY_ID | NUMBER | Primary Key |
| CATEGORY_NAME | VARCHAR2(100) | Category Name |
| DESCRIPTION | VARCHAR2(300) | Category Description |
| CREATED_AT | TIMESTAMP | Record creation time |

---

# 3. COMPLAINTS Table

## Purpose

Stores complaints submitted by citizens.

Each complaint belongs to:

- One User
- One Issue Category

## Columns

| Column | Data Type | Description |
|---------|-----------|-------------|
| COMPLAINT_ID | NUMBER | Primary Key |
| USER_ID | NUMBER | Foreign Key (USERS) |
| CATEGORY_ID | NUMBER | Foreign Key (ISSUE_CATEGORIES) |
| TITLE | VARCHAR2(150) | Complaint Title |
| DESCRIPTION | VARCHAR2(1000) | Complaint Description |
| LOCATION | VARCHAR2(255) | Complaint Location |
| LATITUDE | NUMBER | GPS Latitude |
| LONGITUDE | NUMBER | GPS Longitude |
| STATUS | VARCHAR2(20) | Complaint Status |
| PRIORITY | VARCHAR2(10) | Complaint Priority |
| CREATED_AT | TIMESTAMP | Complaint Created Time |
| UPDATED_AT | TIMESTAMP | Last Updated Time |

---

# Relationships

## USERS → COMPLAINTS

Relationship:

One User can create many Complaints.

```
USERS (1)
      |
      |
      |------< COMPLAINTS (Many)
```

---

## ISSUE_CATEGORIES → COMPLAINTS

Relationship:

One Category can contain many Complaints.

```
ISSUE_CATEGORIES (1)
          |
          |
          |------< COMPLAINTS (Many)
```

---

# Primary Keys

| Table | Primary Key |
|---------|-------------|
| USERS | USER_ID |
| ISSUE_CATEGORIES | CATEGORY_ID |
| COMPLAINTS | COMPLAINT_ID |

---

# Foreign Keys

| Child Table | Foreign Key | Parent Table |
|--------------|-------------|--------------|
| COMPLAINTS | USER_ID | USERS |
| COMPLAINTS | CATEGORY_ID | ISSUE_CATEGORIES |

---

# Constraints Used

- PRIMARY KEY
- FOREIGN KEY
- NOT NULL
- UNIQUE
- CHECK
- DEFAULT

---

# Database Features

- Unique email for every user.
- Each complaint belongs to a valid user.
- Each complaint belongs to a valid category.
- Complaint status is controlled using CHECK constraints.
- Complaint priority is limited to predefined values.
- Automatic timestamp generation for records.

---

# Future Database Expansion

In the next development phases, the following tables will be added:

- DEPARTMENTS
- WORKERS
- ASSIGNMENTS
- COMPLAINT_IMAGES
- FEEDBACK
- UPVOTES
- STATUS_HISTORY

These tables will extend the current database while maintaining proper relational integrity.

---

# ER Diagram (Conceptual)

```
               USERS
             +---------+
             | USER_ID |
             +---------+
                  |
                  | 1
                  |
                  | N
          +----------------+
          |   COMPLAINTS   |
          +----------------+
          | COMPLAINT_ID   |
          | USER_ID (FK)   |
          | CATEGORY_ID(FK)|
          +----------------+
                  ^
                  |
                  | N
                  |
                  | 1
       +----------------------+
       | ISSUE_CATEGORIES     |
       +----------------------+
       | CATEGORY_ID          |
       +----------------------+
```

---

# Conclusion

The current database design provides a strong foundation for the CivicPulse system. It ensures data integrity through primary keys, foreign keys, and constraints while remaining scalable for future modules such as department management, worker assignment, complaint tracking, image uploads, and citizen feedback.