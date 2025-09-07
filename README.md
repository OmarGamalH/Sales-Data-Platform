# Sales Data Platform 
## Overview

a production‑minded sales data platform that integrates data lake and data warehouse patterns to deliver reliable, analytics‑ready data. Apache NiFi ingests from OLTP into HDFS (Parquet, bronze), Apache Airflow orchestrates PySpark transformations into a curated Silver layer, and PostgreSQL exposes Gold views for BI and reporting. Data quality is embedded end‑to‑end with PyDeequ


---
## Table of Contents
- [Data Architecture](#data-architecture)
- [Data Modeling](#data-modeling)
- [Data Ingestion (NiFi)](#data-ingestion-nifi)
- [Airflow Orchestration](#airflow-orchestration)
- [SQL Queries](#sql-queries)
- [Setup & Additional Info](#setup--additional-info)
- [Documentation](#documentation)
---

# Data Architecture

## Architecture Overview



<img width="1052" height="450" alt="Image" src="https://github.com/user-attachments/assets/f49b980c-bbf2-42e9-8a9e-6b6ed793206d" />

---

### Components Breakdown

#### 1. **Sources**
- **Sales Data (OLTP)**: Raw sales transactional data stored in a relational database (e.g., SQL Server).

#### 2. **Data Ingestion**
- **Apache NiFi**: Handles the extraction and ingestion of data from source systems into the data lake. NiFi provides robust, scalable, and traceable data pipelines, ensuring secure and reliable movement of data.

#### 3. **Data Lake**
- **HDFS (Bronze Layer)**: Raw ingested data is stored in Hadoop Distributed File System (HDFS) in its native format. This layer acts as the immutable storage of raw data.

#### 4. **ETL (Spark)**
- **Apache Spark**: Performs Extract, Transform, Load (ETL) operations on the bronze data, cleaning, validating, and transforming it for further processing.

#### 5. **Silver Layer (Processed Data)**
- **Processed Data**: After ETL, data is stored in the Silver layer, representing cleansed and conformed datasets ready for analytics and further transformation.

#### 6. **Gold Layer (Aggregated Data)**
- **Aggregated Data**: The Gold layer contains aggregated, business-ready datasets, optimized for reporting and analytics.

#### 7. **Data Warehouse**
- **PostgreSQL**: Aggregated sales data is loaded into a PostgreSQL database for advanced analytics, reporting, and BI consumption.

#### 8. **Data Consumption**
- **Power BI Dashboards**: Business users and analysts access curated datasets through interactive Power BI dashboards for insights and decision-making.

---

### Orchestration & Quality Management

- **Data Orchestration (Airflow)**: All data movement and transformation processes are orchestrated using Apache Airflow, ensuring scheduled and automated workflow execution.
- **Data Quality Management (deequ)**: Data quality checks are implemented using Deequ, enforcing validation on ingested and processed datasets.

---

## Data Flow Summary

1. **Extract**: Sales data is ingested from OLTP sources via Apache NiFi.
2. **Load**: Raw data lands in the HDFS (Bronze Layer).
3. **Transform**: Spark ETL jobs process the raw data, moving cleansed data to the Silver layer.
4. **Aggregate**: Further transformations produce business aggregates in the Gold layer.
5. **Warehouse**: Aggregated data is loaded into PostgreSQL for downstream consumption.
6. **Consume**: Power BI dashboards provide data-driven insights to stakeholders.

---

## Technologies Used

- **Apache NiFi**: Data ingestion and movement.
- **Apache Spark**: Distributed data processing and transformation.
- **HDFS**: Scalable storage for raw and processed data.
- **Apache Airflow**: Workflow orchestration.
- **Deequ**: Data quality monitoring.
- **PostgreSQL**: Data warehousing.
- **Power BI**: Business intelligence and visualization.

---

## Extensibility

This architecture can be extended to support additional data sources, new transformation logic, or integration with other BI tools and storage technologies.

---

# Data Modeling

## OLTP Data Model

The OLTP model is optimized for transactional operations, such as capturing sales orders, managing customers, and processing payments. It is highly normalized to ensure data integrity and minimize redundancy.

### Conceptual Data Model

The conceptual model defines the main business entities and their relationships in the sales process:

<img width="1062" height="798" alt="Image" src="https://github.com/user-attachments/assets/b5634455-941a-46f3-a5c6-22f9f9244c2d" />

### Logical Data Model

The logical model details the structure and attributes of each entity, including primary keys, foreign keys, and column types:

<img width="1340" height="797" alt="Image" src="https://github.com/user-attachments/assets/a9eb3bf3-50cf-46af-8776-fb971a208a03" />

---

## OLAP Data Model

The OLAP model is designed for analytical processing, supporting complex queries, aggregations, and reporting. It follows a star schema or snowflake schema structure to improve query performance and usability for BI tools.

### Conceptual Data Model

The conceptual OLAP model shows how fact and dimension tables are related:

<img width="1057" height="777" alt="Image" src="https://github.com/user-attachments/assets/1f3d74eb-3484-4f2e-b50b-3b2331330bdd" />

### Logical Data Model

The logical OLAP model details the schema structure for analytics:

<img width="1483" height="833" alt="Image" src="https://github.com/user-attachments/assets/92964589-e8cb-487a-88ec-f0f3c4346b1a" />

---

## Star Schema Overview

The primary analytical model is a star schema, consisting of a central fact table (**Fact_SalesOrder**) and several dimension tables. This schema enables fast, flexible querying and aggregation.

<!-- ### Star Schema ERD

![OLAP Star Schema ERD](Image2.png) <!-- Update path if needed -->

**Fact Table:**  
- `Fact_SalesOrder`: Contains transactional sales data (order details, financials, dates, etc.). -->

**Dimension Tables:**  
- `Dim_Person`: Customer and salesperson information.
- `Dim_Store`: Store details.
- `Dim_Territory`: Sales territory information.
- `Dim_Address`: Shipping and billing address details.
- `Dim_CreditCard`: Credit card attributes.
- `Dim_ShipMethod`: Shipping method details.
- `Dim_CurrencyRate`: Currency conversion rates.

---

<!-- ## Physical Data Model

The physical model shows the actual structure and relationships of tables as implemented in the platform.

### OLAP Physical Data Model (Silver Layer Example)
![Physical Data Model - OLAP](Image3.png)

### OLTP Physical Data Model (Example)
![Physical Data Model - OLTP](Image5.png)

--- -->

<!-- ## Entity Relationship Diagrams

Below are the ER diagrams representing the OLTP and OLAP data models, including primary keys, foreign keys, and table attributes.

### OLAP ER Diagram (Business-Oriented)
![OLAP Business ERD](Image4.png)

--- -->

## Key Design Principles

- **Normalization (OLTP):** Ensures data integrity, avoids duplication, and supports efficient write operations.
- **Denormalization (OLAP):** Enables fast aggregations, reporting, and analytics.
- **Clear Separation:** OLTP and OLAP models are separated for optimized performance and scalability.
- **Extensibility:** Models are designed to support future business requirements and additional data sources.

---

## How to Use

- **OLTP Schema:** Use for transactional operations and source data ingestion.
- **OLAP Schema:** Use for analytics, reporting, and BI dashboarding.

---

# Data Ingestion (NiFi)

## Overview

This project uses Apache NiFi to orchestrate ingestion from OLTP (SQL Server/AdventureWorks2022) into an HDFS-based Data Lake. The current workflow is modeled as importable NiFi JSON process groups (included in this repo) and illustrated by the images below.

Key characteristics:
- Visual, reliable, and traceable ingestion
- Repeatable batch extracts per source table
- Columnar storage using Parquet (GZIP compression) for analytics
- Companion JSON metadata persisted from FlowFile attributes
- Optional downstream orchestration trigger via HTTP (e.g., Airflow)

---

## NiFi Pipeline Architecture 

Each table-level process group follows the same processor chain:

1. ExecuteSQL (2.4.0)
      - Runs a table-specific SELECT using a shared DBCP connection pool service: AdventureWorks2022
      - Emits Avro FlowFiles

2. ConvertAvroToParquet (2.5.0)

      - Converts Avro content to Parquet with GZIP compression

3. UpdateAttribute (2.4.0)
      - Sets a deterministic Parquet filename (e.g., Address.parquet, Customer.parquet, …)

4. PutHDFS (2.5.0)
      - Writes Parquet files to HDFS directory: /nifi_dest/files/
      - Conflict Resolution Strategy: replace
      - Writing Strategy: writeAndRename

5. AttributesToJSON (2.4.0)
      - Serializes FlowFile attributes (including core attributes) into JSON in the FlowFile content

6. UpdateAttribute (2.4.0)
    - Renames the JSON file by replacing parquet with json in the filename expression (e.g., Address.json)

7. PutHDFS (2.5.0)
      - Writes JSON metadata to HDFS directory: /nifi_dest/attributes/
      - Conflict Resolution Strategy: append
      - Writing Strategy: writeAndRename

8. Output Port
      - Each group exposes a terminal Output Port to signal downstream routing within the NiFi canvas

Airflow/External Orchestration (optional):

   - Separate “Airflow Triggering” process group with InvokeHTTP configured to POST to a target endpoint after ingestion.
   - Example URL (from JSON): http:/localhost:8080/api/v2/assets/26/materialize
   - Adjust protocol/host/path and authentication (OAuth2/Basic/etc.) as needed 
   - Adjust the asset id in the URL to match with id used Ex : http:/localhost:8080/api/v2/assets/{asset_id}/materialize

---

## Controller Services

- DBCPConnectionPool: AdventureWorks2022
  - Driver: com.microsoft.sqlserver.jdbc.SQLServerDriver
  - URL: jdbc:sqlserver://<host>:1433;databaseName=AdventureWorks2022;trustservercertificate=true
  - Driver Location: /usr/local/nifi/sqljdbc/enu/jars/mssql-jdbc-12.10.1.jre11.jar
  - Provide credentials (Password) securely at runtime; do not commit secrets.

Notes:

- ConvertAvroToParquet uses compression-type: GZIP.
- PutHDFS processors use Resource Transfer Source: FLOWFILE_CONTENT.
- All processors are configured TIMER_DRIVEN with default scheduling; tune according to workload.

---

## Process Groups (tables)

The repository contains a process group per table. Each group implements the chain described above with table-specific SQL and filenames:

- Address

      - SQL: SELECT AddressID, AddressLine1, AddressLine2, City, StateProvinceID, PostalCode, ModifiedDate FROM Person.Address
      - Output files: Address.parquet → /nifi_dest/files/, Address.json → /nifi_dest/attributes/
      - Output Port: AddressOutput

- SalesOrderHeader

      - SQL: SELECT * FROM Sales.SalesOrderHeader
      - Output files: SalesOrderHeader.parquet / SalesOrderHeader.json
      - Output Port: SalesOrderHeaderOutput

- CreditCard

      - SQL: SELECT * FROM Sales.CreditCard
      - Output files: CreditCard.parquet / CreditCard.json
      - Output Port: CreditCardOutput

- Customer

      - SQL: SELECT * FROM Sales.Customer
      - Output files: Customer.parquet / Customer.json
      - Output Port: CustomerOutput

- CurrencyRate

      - SQL: SELECT * FROM Sales.CurrencyRate
      - Output files: CurrencyRate.parquet / CurrencyRate.json
      - Output Port: CurrencyRateOutput

- Person

      - SQL: SELECT BusinessEntityID, PersonType, NameStyle, Title, FirstName, MiddleName, LastName, Suffix, EmailPromotion, ModifiedDate FROM Person.Person
      - Output files: Person.parquet / Person.json
      - Output Port: PersonOutput

- ShipMethod

      - SQL: SELECT * FROM Purchasing.ShipMethod
      - Output files: ShipMethod.parquet / ShipMethod.json
      - Output Port: ShipMethodOutput

- Store

      - SQL: SELECT * FROM Sales.Store
      - Output files: Store.parquet / Store.json
      - Output Port: StoreOutput

- Territory

      - SQL: SELECT * FROM Sales.SalesTerritory
      - Output files: SalesTerritory.parquet / SalesTerritory.json
      - Output Port: TerritoryOutput

Airflow Triggering

- InvokeHTTP POST to trigger downstream orchestration (e.g., an Airflow DAG or a materialization API).
- Configure URL, headers, authentication, and failure handling to match your environment.

---

## Flow Notes

- Each table group has:
  - One input port (internal wiring) and one output port (terminal) for clear flow boundaries.
  - Two HDFS sinks:
    - /nifi_dest/files/ for Parquet data
    - /nifi_dest/attributes/ for JSON metadata
- File naming is controlled via UpdateAttribute:
  - Parquet: <TableName>.parquet
  - JSON: filename expression replaces “parquet” with “json”
- Parquet writer uses GZIP compression for efficient analytics storage.
- AttributesToJSON includes core attributes and writes pretty-printed=false by default.

---

## Flow Definitions (JSON) locations

Relative to the repository root:

- Apache Nifi/
  - Individual Flows/
    - Address_table.json
    - Airflow_Triggering.json
    - CreditCard_table.json
    - CurrencyRate_table.json
    - Customer_table.json
    - Person_table.json
    - SalesOrderHeader_table.json
    - ShipMethod_table.json
    - Store_table.json
    - Territory_table.json
  - Whole Flow/
    - Sales_Data_Platform_Project.json

Notes:

- “Individual Flows” contains one process group per table plus the Airflow trigger group.
- “Whole Flow” contains an end-to-end project-level process group covering the entire pipeline.

---

## Importing and Running the Flows

1. In NiFi, use “flow definition” to import the JSON files found in this repo (one per process group).
2. Enable the AdventureWorks2022 DBCP connection pool service and set the database password securely.
3. Ensure the HDFS client configuration is available to NiFi and that /nifi_dest/files/ and /nifi_dest/attributes/ are accessible.
4. Start processors in each group or orchestrate starts from a parent process group.
5. Optionally enable the “Airflow Triggering” group and configure InvokeHTTP with your environment’s URL and auth.

---

## Images Overview

### Project’s Process Group Workflow
<img width="1522" height="453" alt="Image" src="https://github.com/user-attachments/assets/b1b6d62e-bf32-4227-93cb-508efa70deb7" />

### Address Process Group 
<img width="1442" height="545" alt="Image" src="https://github.com/user-attachments/assets/f31f04aa-97e3-4a50-9b67-9e4d5cdf7a0b" />

---

# Airflow Orchestration

## Overview

Apache Airflow orchestrates the end-to-end ETL pipeline after ingestion by Apache NiFi. The pipeline is organized into task groups per domain/table with a consistent pattern:

- Before Data Profile (BDP): Run data quality profiling on raw parquet prior to transformations.
- ETL: Transform the dataset and load it into the PostgreSQL data warehouse (Silver layer).
- After Data Profile (ADP): Run data quality profiling on the loaded table to validate the result.

The DAG is event-driven. NiFi invokes the DAG via HTTP (using InvokeHTTP), linking ingestion and transformation in a single operational flow.

---

## Repository paths (relative to repo root)

- DAG

        dags/SalesDataPlatform.py

- Utilities and Data Quality

        dags/Utilities/Utilities.py
        dags/Utilities/DataQuality.py
        dags/Utilities/logs.log
        dags/Utilities/artifacts/  (for auxiliary outputs such as archived duplicates)

- Documentation assets

        documentation/docs/assets/Airflow Dag.png

- Data locations referenced by the DAG

        HDFS source parquet: hdfs:/nifi_dest/files/
        HDFS duplicates mapping archive: hdfs:/nifi_dest/duplicates_mapping/

- Warehouse targets (see SQL scripts in SQL Queries/)

        Database: salesdatawarehouse
        Schemas: silver, dataquality

---

## Architecture

1. Ingestion: NiFi extracts from OLTP, produces parquet in HDFS, then triggers Airflow via HTTP.
2. Orchestration: Airflow runs a single DAG with sequential task groups per table/domain.
3. Processing: Each group executes BDP → ETL → ADP using shared Utilities functions and Deequ-based quality checks.
4. Storage:

        - Silver schema: curated dimensional and fact tables
        - DataQuality schema: Deequ metrics snapshots “Before” and “After” ETL

DAG overview image:

<img width="1917" height="907" alt="Image" src="https://github.com/user-attachments/assets/6ff8ab1c-e7f9-4e91-85a1-cc3fde05adb5" />


---

## The DAG: SalesDataPlatfromDag

Source: dags/SalesDataPlatform.py

- Scheduling model:

        - @asset(schedule=None) creates an asset named SalesTables (no periodic schedule).
        - The DAG uses that asset as the schedule parameter: @dag(schedule=SalesTables)
        - Result: the DAG is designed for external triggering (e.g., NiFi InvokeHTTP or manual UI trigger).

- Execution order (task groups):
  Address → CreditCard → ShipMethod → Territory → Store → Person → CurrencyRate → SalesOrderHeader_Customer

- Pattern inside each group:

        - BDP: Profile raw parquet and write metrics to dataquality schema.
        - ETL: Read parquet, transform via Utilities, write to silver schema.
        - ADP: Profile silver table and write metrics to dataquality schema.

---

## Task Groups and Tasks

Below is a concise description of each group, its tasks, and destinations.

- Address

        - AddressBDP: parquet Address.parquet → DataQuality.Address (status: “Before”)
        - AddressETL: Utilities.AddressTransform → load to silver.dimaddress
        - AddressADP: profile silver.dimaddress → DataQuality.Address (status: “After”)

- CreditCard

        - CreditCardBDP: parquet CreditCard.parquet → DataQuality.CreditCard (“Before”)
        - CreditCardETL: Utilities.CreditCardTransform → load to silver.dimcreditcard
        - CreditCardADP: profile silver.dimcreditcard → DataQuality.CreditCard (“After”)

- ShipMethod

        - ShipMethodBDP: parquet ShipMethod.parquet → DataQuality.ShipMethod (“Before”)
        - ShipMethodETL: Utilities.ShipMethodTransform → load to silver.DimShipMethod
        - ShipMethodADP: profile silver.DimShipMethod → DataQuality.ShipMethod (“After”)

- Territory

        - TerritoryBDP: parquet SalesTerritory.parquet → DataQuality.Territory (“Before”)
        - TerritoryETL: Utilities.TerritoryTransform → load to silver.DimTerritory
        - TerritoryADP: profile silver.DimTerritory → DataQuality.Territory (“After”)

- Store

        - StoreBDP: parquet Store.parquet → DataQuality.Store (“Before”)
        - StoreDuplicatesSaving: Utilities.GetFKReplacement + archive mapping to hdfs:/nifi_dest/duplicates_mapping/Store
        - StoreETL: Utilities.StoreTransform → load to silver.DimStore
        - StoreADP: profile silver.DimStore → DataQuality.Store (“After”)

- Person

        - PersonBDP: parquet Person.parquet → DataQuality.Person (“Before”)
        - PersonETL: Utilities.PersonTransform → load to silver.DimPerson
        - PersonADP: profile silver.DimPerson → DataQuality.Person (“After”)

- CurrencyRate

        - CurrencyRateBDP: parquet CurrencyRate.parquet → DataQuality.CurrencyRate (“Before”)
        - CurrencyRateETL: Utilities.CurrencyRateTransform → load to silver.DimCurrencyRate
        - CurrencyRateADP: profile silver.DimCurrencyRate → DataQuality.CurrencyRate (“After”)

- SalesOrderHeader_Customer (Fact)

        - SalesBDP: parquet SalesOrderHeader.parquet → DataQuality.SalesOrderHeader (“Before”)
        - SalesETL: Utilities.FactSalesTransform(Sales, Customer) → load to silver.FactSales
        - SalesADP: profile silver.FactSales → DataQuality.SalesOrderHeader (“After”)

---

## Utilities module

Source: dags/Utilities/Utilities.py

- Spark session and dependencies:

        - Adds PostgreSQL JDBC driver 
        - Integrates Deequ 

- IO helpers:

        - extract_parquet
        - load_to_postgresql
        - extract_postgres
    

- Duplicates handling:

        - GetFKReplacement
        - load_to_duplicates_archive
        - extract_duplicates_mapping
        - proccess_duplicates

- Transformations:

        - AddressTransform
        - CreditCardTransform
        - ShipMethodTransform
        - TerritoryTransform
        - StoreTransform
        - PersonTransform
        - CurrencyRateTransform
        - FactSalesTransform

- Logging:

        - Python logging to dags/Utilities/logs.log
        - Reduces PySpark/py4j log verbosity

---

## Data Quality module

Source: dags/Utilities/DataQuality.py

- Framework: PyDeequ with Spark
- Pattern:

        - Build analyzers per dataset
        - Run AnalysisRunner to compute metrics
        - Convert metrics to a DataFrame
        - Utilities.DataQualityProcessing adds TableName, Status (“Before”/“After”), timestamps, and aligns column names
        - Load to PostgreSQL schema dataquality via Utilities.load_to_postgresql
---

## Operational considerations

- Triggering:

        - Externally via NiFi InvokeHTTP or manually via Airflow UI “Trigger” button.
        - The DAG is designed for on-demand runs (no CRON schedule attached to the asset).

- Idempotency and deduplication:

        - Warehouse-side: BEFORE INSERT triggers (see SQL Queries/TriggersCreation.sql) delete existing rows by PK before insert.
        - Pipeline-side: Store duplicates are archived and a mapping is applied in FactSales to ensure consistent foreign keys.

- Dependencies:

        - The sequential task-group chain enforces referential integrity and ensures dimensions load before the fact.

- Monitoring and logs:

        - Task logs available in the Airflow UI.
        - Application-level logs written to dags/Utilities/logs.log.
        - Deequ metrics captured in the dataquality schema for “Before” and “After.”
---

## End-to-end flow

1. NiFi writes parquet files and triggers the DAG.
2. For each domain/table:

        - BDP computes metrics on raw parquet and writes to DataQuality.
        - ETL transforms the dataset and loads to Silver.
        - ADP re-profiles the loaded table and writes to DataQuality.

3. After all dimensions complete, the fact pipeline runs (SalesOrderHeader + Customer → FactSales).
4. Gold-layer objects (e.g., Gold.FullView) are created via SQL scripts and can be materialized downstream.

---

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

---

# Setup & Additional Info

## Prerequisites
- Docker (recommended for local setup)
- Python 3.9+
- Java 11+ (for NiFi, Spark)
- PostgreSQL
- pyspark
- [Optional] Power BI Desktop

## Setup Steps

1. Clone the Repository
   ```bash
   git clone https://github.com/OmarGHamed/Sales-Data-Platform.git
   cd Sales-Data-Platform
   ```
2. Run "Run_This_Once.sh" only once to initialize the packages directory that will be used in Airflow.
3. Run "Start_Components.sh" to start all components (Hadoop, NiFi, Airflow).
4. Start Database: Create the PostgreSQL database and schemas using the SQL scripts referenced in Sql.md.
5. Run Initial Data Ingestion: Use the NiFi UI to trigger workflows, verify HDFS data, and trigger the Airflow DAG via NiFi.
6. Check Data Warehouse: Use psql or PgAdmin to inspect loaded tables.
7. Visualize in Power BI: Connect to PostgreSQL and build simple dashboards.

---

## Directory Structure

The following reflects the current repository layout.

### Root Level (./)

- Apache Nifi/
- Data Architecture/
- Data Models/
- README.md
- Run_This_Once.sh
- SQL Queries/
- Start_Components.sh
- dags/
- documentation/

---

### Apache NiFi (./Apache Nifi)

- Individual Flows/
  - Address_table.json
  - Airflow_Triggering.json
  - CreditCard_table.json
  - CurrencyRate_table.json
  - Customer_table.json
  - Person_table.json
  - SalesOrderHeader_table.json
  - ShipMethod_table.json
  - Store_table.json
  - Territory_table.json
- Whole Flow/
  - Sales_Data_Platform_Project.json

---

### Data Architecture (./Data Architecture)

- Project's Data Architecture(Editable version).drawio

---

### Data Models (./Data Models)

- OLAP Conceptual Data Model.drawio
- OLTP Conceptual Data Model.drawio

---

### SQL Queries (./SQL Queries)

- DataWarehouseCreation.sql
- TablesCreation.sql
- TriggersCreation.sql
- ViewsCreation.sql

---

### Airflow DAGs (./dags)

- SalesDataPlatform.py
- Utilities/

        - Utilities.py
        - DataQuality.py
        - __pycache__/            (Python bytecode cache)
        - artifacts/              (currently empty; used for archived outputs)
        - logs.log                (ETL and Spark logs)

---

### Documentation (./documentation)

- docs/

        - Airflow.md
        - Data Architecture.md
        - Data Modeling.md
        - Nifi.md
        - Sql.md
        - assets/
        - index.md
        - last.md  (this file)
- mkdocs.yml

---

### Documentation Assets (./documentation/docs/assets)

- Address.png
- Airflow Dag.png
- Nifi Project workflow.png
- OLAP Logical Data Model.png
- OLAP Conceptual Data Model.png
- OLTP Conceptual data model.png
- OLTP.png
- "Project's Data Architecture.png"

---

# Documentation

For full technical details, guides, diagrams, and explanations, use the MkDocs documentation site.

### How to View the Documentation

1. **Install MkDocs (if not already installed):**
    ```bash
    pip install mkdocs
    ```
2. **Serve the docs locally:**
    ```bash
    cd documentation
    mkdocs serve
    ```
3. **Browse the docs:**
    - Visit [http://localhost:8000](http://localhost:8000) in your browser.
    - Topics include Data Architecture, Data Modeling, NiFi Flows, Airflow ETL, SQL, and more.

---


### Notes

- All code, workflows, and documentation are organized to support modularity, clarity, and ease of navigation.
- Editable diagrams are stored as .drawio files for further updates.
- The documentation site uses MkDocs for easy navigation and search.

---

## License

[MIT](LICENSE)

---

## Author

[OmarGamalH](https://github.com/OmarGamalH)
