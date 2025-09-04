# Sales Data Platform

A modern, modular platform for scalable sales data processing, analytics, and orchestration. This repository provides end-to-end architecture, ETL orchestration, data modeling, and setup instructions for powering advanced business intelligence with technologies like Apache NiFi, Spark, Airflow, PostgreSQL, and Power BI.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
  - [Data Flow](#data-flow)
  - [Component Breakdown](#component-breakdown)
  - [Data Orchestration & Quality](#data-orchestration--quality)
  - [Technologies Used](#technologies-used)
  - [Extensibility](#extensibility)
- [Data Modeling](#data-modeling)
  - [OLTP Model](#oltp-model)
  - [OLAP Model](#olap-model)
  - [Star Schema](#star-schema)
  - [Design Principles](#design-principles)
- [ETL Orchestration](#etl-orchestration)
  - [NiFi Data Ingestion](#nifi-data-ingestion)
  - [Airflow ETL Pipeline](#airflow-etl-pipeline)
- [SQL Data Warehouse](#sql-data-warehouse)
- [Directory Structure](#directory-structure)
- [Setup Guide](#setup-guide)
- [Notes](#notes)

---

## Overview

The **Sales Data Platform** enables efficient and reliable processing of sales data, transforming raw transactional records into curated datasets for analytics and business intelligence. It leverages a lakehouse architecture, orchestrated ETL pipelines, and modular data models to deliver trusted insights.

---

## Architecture

### Data Flow

1. **Extract:** Sales data ingested from OLTP sources via Apache NiFi.
2. **Load:** Raw data lands in the HDFS (Bronze Layer).
3. **Transform:** Spark ETL jobs process raw data into the Silver Layer.
4. **Aggregate:** Further transformations produce business aggregates in the Gold Layer.
5. **Warehouse:** Aggregated data loaded into PostgreSQL for analytics.
6. **Consume:** Power BI dashboards provide interactive insights.

![Data Architecture](documentation/docs/assets/Project's%20Data%20Architecture.png)

---

### Component Breakdown

1. **Sources:**  
   - _Sales Data (OLTP)_: Relational transactional data (e.g., SQL Server).

2. **Data Ingestion:**  
   - _Apache NiFi_: Extracts and ingests data into the data lake with robust, traceable pipelines.

3. **Data Lake:**  
   - _HDFS (Bronze Layer)_: Immutable storage of raw data.

4. **ETL:**  
   - _Apache Spark_: Cleans, validates, and transforms data for analytics.

5. **Silver Layer:**  
   - _Processed Data_: Cleansed, conformed datasets for further transformation.

6. **Gold Layer:**  
   - _Aggregated Data_: Optimized for reporting and analytics.

7. **Data Warehouse:**  
   - _PostgreSQL_: Advanced analytics, reporting, and BI.

8. **Data Consumption:**  
   - _Power BI Dashboards_: Interactive analytics for business users.

---

### Data Orchestration & Quality

- **Airflow:**  
  Orchestrates all data movement and transformation processes with scheduled and automated workflows.

- **Deequ:**  
  Enforces data quality checks on ingested and processed datasets.

---

### Technologies Used

- **Apache NiFi**: Data ingestion and movement
- **Apache Spark**: Distributed processing
- **HDFS**: Scalable storage
- **Apache Airflow**: Workflow orchestration
- **Deequ**: Data quality monitoring
- **PostgreSQL**: Data warehousing
- **Power BI**: Business intelligence

---

### Extensibility

The platform can be extended to support new data sources, transformation logic, BI tools, or storage technologies.

---

## Data Modeling

### OLTP Model

_Optimized for transactional operations and integrity._

- Highly normalized; captures sales orders, customers, payments, etc.
- **Conceptual & Logical Models:**
  ![OLTP Conceptual Data Model](documentation/docs/assets/OLTP%20Conceptual%20data%20model.png)
  ![OLTP Logical Data Model](documentation/docs/assets/OLTP.png)

---

### OLAP Model

_Designed for analytical processing and reporting._

- Star/snowflake schemas for fast querying and aggregations.
- **Conceptual & Logical Models:**
  ![OLAP Conceptual Data Model](documentation/docs/assets/OLAP%20Conceptual%20Data%20Model.png)
  ![OLAP Logical Data Model](documentation/docs/assets/OLAP%20Logical%20Data%20Model.png)

---

### Star Schema

- **Fact Table:**  
  - `Fact_SalesOrder`: Transactional sales data (order details, financials, dates).
- **Dimension Tables:**  
  - `Dim_Person`, `Dim_Store`, `Dim_Territory`, `Dim_Address`, `Dim_CreditCard`, `Dim_ShipMethod`, `Dim_CurrencyRate`

#### Design Principles

- **Normalization (OLTP):** Data integrity, efficient writes.
- **Denormalization (OLAP):** Fast aggregations, reporting.
- **Separation:** OLTP and OLAP are separated for performance and scalability.
- **Extensibility:** Models support future requirements and new data sources.

---

## ETL Orchestration

### NiFi Data Ingestion

_Visual, traceable ETL backbone connecting OLTP sources to the Data Lake._

- **Extraction:**  
  - `ExecuteSQL` processors for source tables (SalesOrderHeader, Address, CreditCard, etc.)
- **Transformation:**  
  - `UpdateAttribute`, `ConvertAvroToParquet`, `AttributesToJSON`
- **Loading:**  
  - `PutHDFS` for storage, `InvokeHTTP` to trigger Airflow DAGs

**NiFi Pipeline Overview:**

![Whole Workflow](documentation/docs/assets/Nifi%20Project%20workflow.png)
![Address Process Group](documentation/docs/assets/Address.png)

---

### Airflow ETL Pipeline

_Apache Airflow orchestrates ETL workflows for loading and transforming data into the warehouse._

- **Integration:**  
  - NiFi triggers Airflow DAG (`SalesDataPlatfromDag`) via REST API.
- **DAG Structure:**  
  - Modular task groups for each table (AddressETL, CreditCardETL, ShipMethodETL, etc.)
  - Sequential execution ensures dependencies and referential integrity.
- **Modularity:**  
  - ETL logic encapsulated in `Utilities.py`:  
    - `extract_parquet(filename)`
    - `AddressTransform(df)`
    - `CreditCardTransform(df)`
    - `FactSalesTransform(sales_df, customer_df)`
    - `load_to_postgresql(df, database, schema, table)`

**Airflow DAG Overview:**

![Airflow DAG](documentation/docs/assets/Airflow%20Dag.png)

---

## SQL Data Warehouse

- **Creation:**  
  - `DataWarehouseCreation.sql`: Sets up main database and schemas (MetaData, Silver, Gold).
- **Tables:**  
  - `TablesCreation.sql`: Dimension and fact tables in Silver layer.
- **Triggers:**  
  - `TriggersCreation.sql`: Upsert logic to ensure deduplication and replace records on insert.

---

## Directory Structure

```
├── Apache Nifi/
│   ├── Individual Flows/
│   │   ├── Address_table.json
│   │   ├── ...
│   ├── Whole Flow/
│       └── Sales_Data_Platform_Project.json
├── Data Architecture/
│   └── Project's Data Architecture(Editable version).drawio
├── Data Models/
│   ├── OLAP Conceptual Data Model.drawio
│   ├── OLTP Conceptual Data Model.drawio
├── SQL Queries/
│   ├── DataWarehouseCreation.sql
│   ├── TablesCreation.sql
│   └── TriggersCreation.sql
├── dags/
│   ├── SalesDataPlatform.py
│   └── Utilities/
│       ├── Utilities.py
│       ├── artifacts/
│       ├── logs.log
├── documentation/
│   ├── docs/
│   │   ├── Airflow.md
│   │   ├── Data Architecture.md
│   │   ├── Data Modeling.md
│   │   ├── Nifi.md
│   │   ├── Sql.md
│   │   ├── assets/
│   │   │   └── [images]
│   │   ├── index.md
│   │   └── last.md
│   └── mkdocs.yml
├── README.md
├── Run_This_Once.sh
├── Start_Components.sh
```

---

## Setup Guide

### Prerequisites

- Docker (recommended for local setup)
- Python 3.9+
- Java 11+ (for NiFi, Spark)
- PostgreSQL
- pyspark
- [Optional] Power BI Desktop

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/OmarGHamed/Sales-Data-Platform.git
    cd Sales-Data-Platform
    ```
2. **Initialize Packages**
    ```bash
    ./Run_This_Once.sh
    ```
3. **Start Platform Components**
    ```bash
    ./Start_Components.sh
    ```
    _(Starts Hadoop, NiFi, Airflow)_

4. **Setup Database**
    - Create PostgreSQL database using scripts in `SQL Queries/Sql.md`.

5. **Run Initial Data Ingestion**
    - Use NiFi UI to trigger workflows.
    - Verify HDFS storage and trigger Airflow DAG via NiFi.

6. **Inspect Data Warehouse**
    - Use `psql` or PgAdmin to check tables.

7. **Visualize in Power BI**
    - Connect to PostgreSQL and build dashboards.

---

## Notes

- Editable diagrams are stored as `.drawio` files.
- Documentation is organized for modularity, clarity, and ease of navigation.
- MkDocs powers the documentation site for browsing and search.
- All ETL code, workflows, and documentation support extensibility and future growth.

---

## License

[MIT](LICENSE)

---

## Author

OmarGHamed
