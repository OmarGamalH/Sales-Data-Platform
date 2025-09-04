# Data Modeling for Sales Data Platform

This document provides an overview of the data modeling approach used in the Sales Data Platform, covering both OLTP (Online Transaction Processing) and OLAP (Online Analytical Processing) systems. The data models are designed to support scalable, accurate, and efficient data analysis, reporting, and business intelligence.

---

## OLTP Data Model

The OLTP model is optimized for transactional operations, such as capturing sales orders, managing customers, and processing payments. It is highly normalized to ensure data integrity and minimize redundancy.

### Conceptual Data Model

The conceptual model defines the main business entities and their relationships in the sales process:

![OLTP Conceptual Data Model](assets/OLTP%20Conceptual%20data%20model.png)

### Logical Data Model

The logical model details the structure and attributes of each entity, including primary keys, foreign keys, and column types:

![OLTP Logical Data Model](assets/OLTP.png)

---

## OLAP Data Model

The OLAP model is designed for analytical processing, supporting complex queries, aggregations, and reporting. It follows a star schema or snowflake schema structure to improve query performance and usability for BI tools.

### Conceptual Data Model

The conceptual OLAP model shows how fact and dimension tables are related:

![OLAP Conceptual Data Model](assets/OLAP%20Conceptual%20Data%20Model.png)

### Logical Data Model

The logical OLAP model details the schema structure for analytics:

![OLAP Logical Data Model](assets/OLAP%20Logical%20Data%20Model.png)

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

