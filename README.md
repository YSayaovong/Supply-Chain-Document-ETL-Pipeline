# **ETL Pipeline: Employee Data → GCS → BigQuery → Masked View → Visualization**

This project is a complete end-to-end **cloud-based ETL pipeline** built with Python, Google Cloud Storage, BigQuery, and basic data visualization.  

It simulates employee data, securely processes it, loads it into BigQuery, masks sensitive fields, and generates analytic insights.

## 📐 **System Architecture**

<img src="https://github.com/YSayaovong/etl-pipeline-datafusion-airflow/blob/main/assets/architecture.PNG" width="800">

This architecture represents the full flow:

1. **Extract** employee data (synthetic) using Python  
2. **Load** the CSV into **Google Cloud Storage**  
3. **Ingest** GCS data into **BigQuery**  
4. **Transform & Mask** sensitive attributes  
5. **Analyze & Visualize** insights  

## 🧰 **Tech Stack**

<img src="https://github.com/YSayaovong/etl-pipeline-datafusion-airflow/blob/main/assets/tech_stack.PNG" width="800">

### **Tools & Technologies**
- Python 3  
- Faker  
- Google Cloud Storage  
- Google BigQuery  
- Matplotlib  
- db-dtypes  
- Service Account Authentication  

## 🚀 **Pipeline Overview**

### **1. Extract & Generate Data**
Run:
python extract.py

### **2. Load Into BigQuery**
Run:
python load_to_bigquery.py

### **3. Visualization (Bar Chart)**
Run:
python bar_chart.py

## 🔐 **Data Masking Strategy**
- Emails masked
- Phone numbers masked
- Passwords hidden
- Salaries converted to bands
