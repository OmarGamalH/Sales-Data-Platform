# SQL Queries

## Overview

This repository includes SQL scripts to provision the warehouse, create tables, implement upsert-style triggers, and expose an analytical view.

Included files:

- SQL Queries/DataWarehouseCreation.sql
- SQL Queries/TablesCreation.sql
- SQL Queries/TriggersCreation.sql
- SQL Queries/ViewsCreation.sql

---

## 1. Data Warehouse and Schema Creation

File: SQL Queries/DataWarehouseCreation.sql

Provisions the main database and core schemas:

- CREATE DATABASE SalesDataWarehouse;
- CREATE SCHEMA DataQuality; — Schema for data quality logging and metrics.
- CREATE SCHEMA Silver; — Core dimensional and fact layer.
- CREATE SCHEMA Gold; — Presentation and analytics layer.

---

## 2. Table Definitions

File: SQL Queries/TablesCreation.sql

Creates the dimensional and fact tables in Silver, plus a data quality table.

- Dimension tables (Silver):

    - Silver.DimAddress
    - Silver.DimCreditCard
    - Silver.DimTerritory
    - Silver.DimShipMethod
    - Silver.DimStore
    - Silver.DimPerson
    - Silver.DimCurrencyRate

- Fact table (Silver):

    - Silver.FactSales

- Data quality table:

    - DataQuality.DataQuality

Notes:

- Types and constraints are defined per table (primary keys on each dimension, SalesOrderID on the fact table).
- The DataQuality.DataQuality table captures checks with fields such as TableName, Status, Entity, Instance, Name, Value, CreatedAt.

---

## 3. Triggers for Deduplication and Upserts

File: SQL Queries/TriggersCreation.sql

Implements BEFORE INSERT triggers in PL/pgSQL to achieve idempotent upserts. Each trigger deletes any existing row with the same primary key before inserting the new row.

- Silver.DimAddress: FnTrgAddress / TrgAddress
- Silver.DimCreditCard: FnTrgCreditCard / TrgCreditCard
- Silver.DimTerritory: FnTrgTerritory / TrgTerritory
- Silver.DimShipMethod: FnTrgShipMethod / TrgShipMethod
- Silver.DimStore: FnTrgStore / TrgStore
- Silver.DimPerson: FnTrgPerson / TrgPerson
- Silver.DimCurrencyRate: FnTrgCurrencyRate / TrgCurrencyRate
- Silver.FactSales: FnTrgFactSales / TrgFactSales

---

## 4. Analytical View

File: SQL Queries/ViewsCreation.sql

Creates Gold.FullView, a presentation-layer view that joins Silver.FactSales to all related dimensions to provide a denormalized, analytics-ready dataset. It includes:

- Sales facts (amounts, dates, account, status)
- Bill-to and ship-to address attributes
- Credit card attributes
- Person attributes
- Ship method attributes
- Store attributes
- Territory attributes (including Group, YTD, LastYear metrics)
- Currency rate attributes

Join keys align on the foreign keys in Silver.FactSales to their respective dimension primary keys.

---

## Execution order

Recommended order when initializing a fresh environment:

1. DataWarehouseCreation.sql
2. TablesCreation.sql
3. TriggersCreation.sql
4. ViewsCreation.sql