/*=========================================================
  CivicPulse Drop All Tables
  Database : Oracle
  Day 4
=========================================================*/

----------------------------------------------------------
-- Drop Child Table First
----------------------------------------------------------

DROP TABLE COMPLAINTS CASCADE CONSTRAINTS;

----------------------------------------------------------
-- Drop Parent Tables
----------------------------------------------------------

DROP TABLE ISSUE_CATEGORIES CASCADE CONSTRAINTS;

DROP TABLE USERS CASCADE CONSTRAINTS;

COMMIT;