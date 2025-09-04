# Sales Data Platform Architecture

This repository contains the architecture and implementation of the **Sales Data Platform**, designed to enable scalable, reliable, and efficient sales data processing and analytics.

---

## Architecture Overview

The platform follows a modern data lakehouse architecture, orchestrating data flow from source systems to analytics dashboards. Below is a high-level diagram of the architecture:

![Data Architecture](<assets/Project's Data Architecture.png>) 

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


