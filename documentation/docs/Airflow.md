# Airflow Orchestration for Sales Data Platform

## Overview

Apache Airflow is deployed to orchestrate the ETL pipeline for the platform. Each step in the pipeline is modularized as a task group, handling the transformation and loading of individual tables into the data warehouse.

NiFi triggers the Airflow DAG (`SalesDataPlatfromDag`) via REST API calls (using the `InvokeHTTP` processor), integrating ingestion and transformation pipelines in a seamless, event-driven manner.

---

## Architecture

**Flow:**

1. NiFi ingests and prepares data, then invokes Airflow DAG execution via HTTP.
2. Airflow runs the ETL pipeline, executing table-wise transformations and loading tasks.
3. Each step is monitored and logged for traceability and reliability.

**DAG Overview:**

![Airflow Dag](assets/Airflow%20Dag.png)

- Each box is a task group representing a table ETL process.
- Task groups run sequentially, ensuring dependencies and referential integrity.

---

## DAG Tasks & Structure

The DAG `SalesDataPlatfromDag` consists of the following major task groups:

- **AddressETL:** Extract, transform, and load address data.
- **CreditCardETL:** Process credit card information.
- **ShipMethodETL:** Transform and load shipping method data.
- **TerritoryETL:** Handle territory-specific transformations.
- **StoreETL:** Manage store records and deduplication logic.
- **PersonETL:** Transform person (customer, employee) data.
- **CurrencyRateETL:** Process currency conversion rates.
- **SalesETL:** Join and transform sales order and customer data.

Each ETL task:
- Extracts parquet files from the data lake.
- Applies dedicated transformation logic.
- Loads processed data into the PostgreSQL-based data warehouse.

---

## Utilities & Modularity

The Airflow DAG leverages a separate module, **Utilities.py**, which encapsulates all ETL logic, transformation functions, and common helper routines. This modular approach brings several benefits:


**Examples of Modular Functions:**

- `extract_parquet(filename)` — Reads parquet files from HDFS.
- `AddressTransform(df)` — Cleans and formats address data.
- `CreditCardTransform(df)` — Validates and transforms credit card data.
- `FactSalesTransform(sales_df, customer_df)` — Joins and processes sales order and customer data.
- `load_to_postgresql(df, database, schema, table)` — Writes processed data to PostgreSQL warehouse.

All these functions are orchestrated by Airflow’s DAG and tasks, ensuring each step is isolated and reusable.



