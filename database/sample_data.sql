/*=========================================================
  CivicPulse Sample Data
  Database : Oracle
  Day 4
=========================================================*/


----------------------------------------------------------
-- USERS
----------------------------------------------------------

INSERT INTO USERS (
    FULL_NAME,
    EMAIL,
    USER_PASSWORD,
    PHONE_NUMBER,
    ROLE
)
VALUES (
    'Rahul Sharma',
    'rahul@example.com',
    'rahul123',
    '9876543210',
    'Citizen'
);


INSERT INTO USERS (
    FULL_NAME,
    EMAIL,
    USER_PASSWORD,
    PHONE_NUMBER,
    ROLE
)
VALUES (
    'Priya Verma',
    'priya@example.com',
    'priya123',
    '9876543211',
    'Citizen'
);


INSERT INTO USERS (
    FULL_NAME,
    EMAIL,
    USER_PASSWORD,
    PHONE_NUMBER,
    ROLE
)
VALUES (
    'Admin User',
    'admin@civicpulse.com',
    'admin123',
    '9999999999',
    'Admin'
);



----------------------------------------------------------
-- ISSUE CATEGORIES
----------------------------------------------------------

INSERT INTO ISSUE_CATEGORIES (
    CATEGORY_NAME,
    DESCRIPTION
)
VALUES (
    'Pothole',
    'Road potholes and damaged roads'
);


INSERT INTO ISSUE_CATEGORIES (
    CATEGORY_NAME,
    DESCRIPTION
)
VALUES (
    'Garbage',
    'Garbage collection related issues'
);


INSERT INTO ISSUE_CATEGORIES (
    CATEGORY_NAME,
    DESCRIPTION
)
VALUES (
    'Street Light',
    'Broken or non-working street lights'
);


INSERT INTO ISSUE_CATEGORIES (
    CATEGORY_NAME,
    DESCRIPTION
)
VALUES (
    'Water Leakage',
    'Pipeline leakage and water wastage'
);


INSERT INTO ISSUE_CATEGORIES (
    CATEGORY_NAME,
    DESCRIPTION
)
VALUES (
    'Drainage',
    'Blocked drainage and sewage issues'
);



----------------------------------------------------------
-- COMPLAINTS
----------------------------------------------------------

INSERT INTO COMPLAINTS (
    USER_ID,
    CATEGORY_ID,
    TITLE,
    DESCRIPTION,
    LOCATION,
    LATITUDE,
    LONGITUDE,
    STATUS,
    PRIORITY
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL='rahul@example.com'),
    (SELECT CATEGORY_ID FROM ISSUE_CATEGORIES WHERE CATEGORY_NAME='Pothole'),
    'Large Pothole Near Bus Stand',
    'A deep pothole is causing traffic problems.',
    'Main Road, Bus Stand',
    17.9784000,
    79.5941000,
    'Pending',
    'High'
);



INSERT INTO COMPLAINTS (
    USER_ID,
    CATEGORY_ID,
    TITLE,
    DESCRIPTION,
    LOCATION,
    LATITUDE,
    LONGITUDE,
    STATUS,
    PRIORITY
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL='priya@example.com'),
    (SELECT CATEGORY_ID FROM ISSUE_CATEGORIES WHERE CATEGORY_NAME='Garbage'),
    'Garbage Not Collected',
    'Garbage has not been collected for three days.',
    'Hanamkonda Market',
    18.0037000,
    79.5706000,
    'Pending',
    'Medium'
);



INSERT INTO COMPLAINTS (
    USER_ID,
    CATEGORY_ID,
    TITLE,
    DESCRIPTION,
    LOCATION,
    LATITUDE,
    LONGITUDE,
    STATUS,
    PRIORITY
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL='rahul@example.com'),
    (SELECT CATEGORY_ID FROM ISSUE_CATEGORIES WHERE CATEGORY_NAME='Street Light'),
    'Street Light Not Working',
    'Street light has been off for one week.',
    'NIT Warangal Gate',
    17.9835000,
    79.5312000,
    'Verified',
    'Medium'
);


COMMIT;