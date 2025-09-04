# Sales Data Platform

Welcome to the Sales Data Platform – a modular, scalable solution for ingesting, processing, modeling, and analyzing sales data. This project is built using best practices and open-source tools to cover the entire data lifecycle: from raw data ingestion to business intelligence.

---

## Key Features

- **Automated Data Ingestion:** Apache NiFi pipelines extract sales data from OLTP sources and land it in a data lake (HDFS).
- **ETL & Processing:** Apache Spark and Airflow orchestrate transformation, cleaning, and enrichment of data.
- **Data Modeling:** Supports both OLTP (transactional) and OLAP (analytical/star schema) models for storage and reporting.
- **Warehouse & Analytics:** Cleaned and aggregated data is loaded into PostgreSQL for advanced analytics and dashboarding (Power BI).
- **Modular Architecture:** Easily extend with new flows, models, and analytics.
- **Quality & Traceability:** Centralized logging, data quality checks (Deequ), and upsert triggers for reliability.

---

## Architecture Overview

1. **Sources (OLTP):** SQL Server or similar transactional sales databases.
2. **Apache NiFi:** Orchestrates extraction, routing, conversion (e.g., Avro → Parquet), and loads data to HDFS.
3. **Data Lake (HDFS):** Stores raw sales data (Bronze layer).
4. **ETL (Spark + Airflow):** Cleans, transforms, and loads data to Silver (processed) and Gold (aggregated) layers.
5. **Data Warehouse (PostgreSQL):** Hosts dimensional (silver) and fact (gold) tables, ready for BI.
6. **Visualization:** Power BI dashboards connect to the warehouse for reporting.

For architecture diagrams and more, see the MkDocs documentation.

---

## Quickstart & Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/OmarGHamed/Sales-Data-Platform.git
    cd Sales-Data-Platform
    ```

2. **Run Initial Setup**
    - Execute `Run_This_Once.sh` to initialize required packages.
    - Execute `Start_Components.sh` to start Hadoop, NiFi, and Airflow.

3. **Database Setup**
    - Use SQL scripts in `SQL Queries/` (DataWarehouseCreation.sql, TablesCreation.sql, TriggersCreation.sql) to provision PostgreSQL.

4. **Ingest Data**
    - Use NiFi UI to trigger flows and verify HDFS data.
    - NiFi triggers Airflow DAG for ETL orchestration.

5. **Explore and Visualize**
    - Check tables in PostgreSQL using `psql` or PgAdmin.
    - Connect Power BI to PostgreSQL for dashboards.

---

## Repository Structure

- **Apache Nifi/**: NiFi flows (individual tables & whole project)
- **Data Architecture/**: Editable diagrams of platform architecture
- **Data Models/**: Editable OLTP/OLAP data model diagrams
- **SQL Queries/**: Database/table/trigger SQL scripts
- **dags/**: Airflow DAGs and ETL utilities (Python)
- **documentation/**: MkDocs documentation site
- **Run_This_Once.sh & Start_Components.sh**: Setup and component start scripts
- **dockerfile**: Docker configuration
- **README.md**: This file

---

## Documentation

Full technical details, diagrams, data models, and guides are available using MkDocs.

**To view the docs locally:**
```bash
cd documentation
mkdocs serve
```
Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## License

MIT License

---

## Need more details?

For comprehensive explanations, guides, and references, please open the MkDocs documentation. Every major component and workflow is covered there!

---
