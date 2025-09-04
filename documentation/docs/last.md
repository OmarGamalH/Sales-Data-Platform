# Setup & Additional Info

## Prerequisites
- Docker (recommended for local setup)
- Python 3.9+
- Java 11+ (for NiFi, Spark)
- PostgreSQL
- pyspark
- [Optional] Power BI Desktop

## Setup Steps

1. **Clone the Repository**
    ```bash
   git clone https://github.com/OmarGHamed/Sales-Data-Platform.git
   cd Sales-Data-Platform
   ```

2. **Start Database** : Create PostgreSQL database using provided SQL scripts in the `Sql.md` documentation.

3. **Run Initial Data Ingestion** : Use NiFi UI to trigger workflows and verify HDFS data and trigger Airflow DAG via NiFi.

4. **Check Data Warehouse** : Use `psql` or PgAdmin to inspect loaded tables.

5. **Visualize in Power BI** : Connect to PostgreSQL and build simple dashboards.


## Directory Structure


### Root Level (`./`)

- **Apache Nifi/**: Contains NiFi flows and configuration files.
- **Data Architecture/**: Editable data architecture diagrams.
- **Data Models/**: Editable OLTP/OLAP data model diagrams.
- **README.md**: Main project readme.
- **Run_This_Once.sh**: Shell script for initial setup steps.
- **SQL Queries/**: Database creation, table and trigger scripts.
- **Start_Components.sh**: Shell script to start platform components.
- **dags/**: Airflow DAG scripts and utilities.
- **documentation/**: Project documentation site (MkDocs).

---

### Apache NiFi (`./Apache Nifi`)

- **Individual Flows/**: NiFi JSON flows for each table.

    - `Address_table.json`
    - `CreditCard_table.json`
    - `CurrencyRate_table.json`
    - `Customer_table.json`
    - `Person_table.json`
    - `SalesOrderHeader_table.json`
    - `ShipMethod_table.json`
    - `Store_table.json`
    - `Territory_table.json`

- **Whole Flow/**: Complete NiFi flow for the project.
    - `Sales_Data_Platform_Project.json`

---

### Data Architecture (`./Data Architecture`)

- `Project's Data Architecture(Editable version).drawio`: Editable architecture flow diagram.

---

### Data Models (`./Data Models`)

- `OLAP Conceptual Data Model.drawio`: Editable OLAP model diagram.
- `OLTP Conceptual Data Model.drawio`: Editable OLTP model diagram.

---

### SQL Queries (`./SQL Queries`)

- `DataWarehouseCreation.sql`: Database and schema creation.
- `TablesCreation.sql`: All table definitions.
- `TriggersCreation.sql`: Table triggers for upsert logic.

---

### Airflow DAGs (`./dags`)

- `SalesDataPlatform.py`: Main Airflow DAG for ETL orchestration.
- `Utilities/`: Shared utility scripts and artifacts.
    - `Utilities.py`: All ETL transformation and helper functions.
    - `__pycache__/`: Python cache.
    - `artifacts/`: (Empty) For future use.
    - `logs.log`: ETL and Spark logs.

---

### Documentation (`./documentation`)

- `docs/`: All markdown documentation and assets for the project.

    - `Airflow.md`
    - `Data Architecture.md`
    - `Data Modeling.md`
    - `Nifi.md`
    - `Sql.md`
    - `assets/`: Images for docs.
    - `index.md`
    - `last.md` (Quickstart/setup guide)

- `mkdocs.yml`: MkDocs configuration file.

---

### Documentation Assets (`./documentation/docs/assets`)

- `Address.png`
- `Nifi Project workflow.png`
- `OLAP Logical Data Model.png`
- `OLAP Conceptual Data Model.png`
- `OLTP Conceptual data model.png`
- `OLTP.png`
- `"Project's Data Architecture.png"`
- `Airflow Dag.png`

---

### Notes

- All code, workflows, and documentation are organized to support modularity, clarity, and ease of navigation.
- Editable diagrams are stored as `.drawio` files for further updates.
- The documentation site uses MkDocs for easy navigation and search.

