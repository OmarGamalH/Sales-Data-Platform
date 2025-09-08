# Data Ingestion

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
![Whole Workflow](assets/Nifi%20Project%20workflow.png)

### Address Process Group 
![Address Process Group](assets/Address.png)