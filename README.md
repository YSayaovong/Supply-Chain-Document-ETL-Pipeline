# ETL Pipeline: Employee Data → GCS → BigQuery → Masked View → Visualization

## 1. Project Background

As a data engineer building a production-style cloud pipeline from scratch, I designed this end-to-end ETL system to answer a practical question that most synthetic tutorial projects skip entirely:

*How do you move data securely from generation to storage to analysis — while masking sensitive attributes before they ever reach an analyst's hands?*

The pipeline simulates a realistic employee dataset, loads it into Google Cloud Storage, ingests it into BigQuery, applies a masked view over sensitive fields, and surfaces departmental insights through visualization. Every stage reflects decisions a working data engineer would make on a real data team.

The dataset is a **500-row synthetic employee file** generated fresh on each pipeline run, spanning fields across identity, compensation, contact, and department — with five fields flagged as sensitive and handled through BigQuery view-level masking rather than upstream deletion, preserving raw auditability while protecting downstream exposure.

The pipeline is structured around four key engineering decisions:

- **Synthetic data generation** with realistic field distributions using Faker
- **Cloud-first storage** with GCS as the staging layer before warehouse ingestion
- **Separation of raw and masked layers** inside BigQuery using a view-based masking strategy
- **Lightweight visualization** on top of the masked view to validate downstream usability

---

## 2. System Architecture

<img src="https://github.com/YSayaovong/etl-pipeline-datafusion-airflow/blob/main/assets/architecture.PNG" width="800">

The architecture follows a five-stage linear flow with a clean handoff between each layer:

| Stage | Step | Tool | Output |
|---|---|---|---|
| 1 | Extract & Generate | Python + Faker | `employee_data.csv` |
| 2 | Upload to Staging | Google Cloud Storage | GCS Blob |
| 3 | Ingest to Warehouse | BigQuery Load Job | Raw Table |
| 4 | Mask Sensitive Fields | BigQuery View | Masked View |
| 5 | Analyze & Visualize | Python + Matplotlib | Department Chart |

The GCS layer serves as the decoupling point between generation and ingestion — mimicking how a real pipeline would receive files from upstream systems (SFTP drops, API exports, flat file transfers) before loading into the warehouse. BigQuery handles both the raw table and the masked view under the same dataset, enabling access-control separation between raw and analytical consumers without duplicating data.

---

## 3. Project Structure

```
etl-pipeline-datafusion-airflow/
│
├── extract.py                      # Generate employee data and upload to GCS
├── load_to_bigquery.py             # Load CSV into BigQuery + create masked view
├── bar_chart.py                    # Query masked view and render department chart
│
├── employee_data.csv               # Synthetic CSV generated on each run
├── employees_by_department.png     # Output chart from bar_chart.py
│
├── assets/
│   ├── architecture.PNG
│   ├── tech_stack.PNG
│   └── employees_by_department.png
│
├── .gitignore                      # Excludes service_account.json from version control
└── README.md
```

---

## 4. Pipeline Overview

### Step 1 — Extract & Generate Data

```bash
python extract.py
```

Generates a 500-row CSV of synthetic employee records using the Faker library. Fields include `employee_id`, `name`, `email`, `phone`, `department`, `salary`, `hire_date`, `job_title`, `password_hash`, and `address`. The output file is written locally as `employee_data.csv` and immediately uploaded to the configured GCS bucket using a Service Account credential. The local file is retained for reference but GCS becomes the authoritative source for downstream steps.

**Fields generated per record:**

| Field | Type | Sensitivity |
|---|---|---|
| employee_id | String (UUID) | Low |
| name | String | Low |
| email | String | **Masked** |
| phone | String | **Masked** |
| department | String | Low |
| salary | Float | **Masked (banded)** |
| hire_date | Date | Low |
| job_title | String | Low |
| password_hash | String | **Masked** |
| address | String | **Masked** |

### Step 2 — Load Into BigQuery

```bash
python load_to_bigquery.py
```

Reads the CSV from GCS using BigQuery's native load job (no intermediate download). Writes to a raw table (`employees_raw`) inside a configured dataset. Immediately after ingestion, creates a `masked_employees` view over the raw table with sensitive fields replaced or transformed. The masked view — not the raw table — is the intended access point for all downstream queries.

### Step 3 — Visualization

```bash
python bar_chart.py
```

Queries the `masked_employees` view via the BigQuery Python client, pulls department and headcount fields, and renders a horizontal bar chart of employee counts by department. Output is saved as `employees_by_department.png`. This step validates that the masked view is queryable end-to-end and that Pandas type handling via `db-dtypes` resolves cleanly for BigQuery result types.

---

## 5. Data Masking Strategy

Masking is applied at the BigQuery view layer — not during generation or upload. This preserves full fidelity in the raw table for audit and reprocessing purposes, while ensuring that any analyst or downstream consumer querying the view never sees sensitive values.

| Field | Raw Value | Masked Value | Strategy |
|---|---|---|---|
| `email` | `john.doe@example.com` | `j***@***.com` | Partial character masking |
| `phone` | `414-555-1234` | `***-***-1234` | Last-4 retention |
| `password_hash` | `5f4dcc3b5aa...` | `[REDACTED]` | Full suppression |
| `salary` | `87,500.00` | `$75K–$100K` | Banded range conversion |
| `address` | `123 Main St, Milwaukee, WI` | `[REDACTED]` | Full suppression |

The banding approach for salary is deliberate: replacing exact compensation with a range bucket preserves analytical utility (headcount by pay band, department compensation distribution) while eliminating the precision that makes salary a PII-equivalent field.

---

## 6. Output
![Employees by Department](https://github.com/YSayaovong/etl-pipeline-datafusion-airflow/blob/main/assets/employees_by_department.png)

The bar chart confirms end-to-end pipeline success — data was generated, uploaded, ingested, masked, and queried successfully. Department distribution reflects Faker's random field generation and is not intended to represent a realistic org structure.

---

## 7. Potential Enhancements

| Enhancement | Value |
|---|---|
| Apache Airflow DAG | Automate scheduling and dependency management across all three pipeline steps |
| dbt transformations | Replace raw SQL view with version-controlled, tested dbt models |
| Partitioned BigQuery tables | Improve query performance and cost control on large datasets |
| Structured logging | Replace print statements with Python `logging` module and Cloud Logging integration |
| Unit tests | Add pytest coverage for data generation, field validation, and masking logic |
| Terraform infrastructure | Define GCS bucket and BigQuery dataset as code for reproducible deployment |

---

## 8. Summary

This pipeline demonstrates a production-style cloud ETL pattern covering synthetic data generation, GCS staging, BigQuery ingestion, view-level data masking, and downstream visualization — end to end in three scripts. The masking strategy reflects a real engineering decision: separating raw storage from analytical access without data duplication or upstream transformation. The GCS staging layer, Service Account authentication pattern, and BigQuery view architecture are directly transferable to enterprise data engineering workflows.

---

## Tools Used

<img src="https://github.com/YSayaovong/etl-pipeline-datafusion-airflow/blob/main/assets/tech_stack.PNG" width="800">

- Python 3 — data generation, GCS upload, BigQuery client, Matplotlib visualization
- Google Cloud Storage — staging layer
- Google BigQuery — raw table + masked view
- Faker — synthetic employee record generation
- Matplotlib — department headcount bar chart
- db-dtypes — BigQuery-to-Pandas type resolution
- Service Account Authentication — GCP credential management
- Git / GitHub — version control
