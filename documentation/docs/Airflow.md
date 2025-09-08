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

![Airflow Dag](assets/Airflow%20Dag.png)


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