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

### Notes

- All code, workflows, and documentation are organized to support modularity, clarity, and ease of navigation.
- Editable diagrams are stored as .drawio files for further updates.
- The documentation site uses MkDocs for easy navigation and search.

