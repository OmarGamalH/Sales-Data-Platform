# SQL Queries


## Overview

The SQL queries in this repository are designed to:

- Create the Data Warehouse and its schemas.
- Define the dimensional and fact tables in the "Silver" layer.
- Implement triggers to handle upserts and maintain consistent, deduplicated data.

---

## 1. Data Warehouse and Schema Creation

**File:** `DataWarehouseCreation.sql`

This script provisions the main database and its organizational schemas:

- `CREATE DATABASE SalesDataWarehouse;` - For Data Warehouse Creation
- `CREATE SCHEMA MetaData;` — For metadata management schema.
- `CREATE SCHEMA Silver;`  — For Silver Layer.
- `CREATE SCHEMA Gold;`    — For Gold Layer.

---

## 2. Table Definitions

**File:** `TablesCreation.sql`

Defines the structure of all core dimension and fact tables in the Silver layer:

- **Dimension Tables:**  

  - `Silver.DimAddress`
  - `Silver.DimCreditCard`
  - `Silver.DimTerritory`
  - `Silver.DimShipMethod`
  - `Silver.DimStore`
  - `Silver.DimPerson`
  - `Silver.DimCurrencyRate`

- **Fact Table:**  

  - `Silver.FactSales`

---

## 3. Triggers for Deduplication and Upserts

**File:** `TriggersCreation.sql`

Implements BEFORE INSERT triggers for each table to ensure upsert (insert or update) behavior and prevent duplicate records:

For each insert:

  - The trigger deletes any existing row with the same primary key.
  - The new row is then inserted, effectively replacing the old record.