from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/project"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="employee_etl_postgres",
    default_args=default_args,
    description="Local ETL: Extract -> Transform -> Load(Postgres) -> Chart",
    schedule_interval=None,     # manual trigger (clean for portfolio)
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command=f'cd {PROJECT_DIR} && python src/extract.py',
    )

    transform = BashOperator(
        task_id="transform",
        bash_command=f'cd {PROJECT_DIR} && python src/transform.py',
    )

    load = BashOperator(
        task_id="load_to_postgres",
        bash_command=f'cd {PROJECT_DIR} && python src/load_to_postgres.py',
    )

    chart = BashOperator(
        task_id="bar_chart",
        bash_command=f'cd {PROJECT_DIR} && python src/bar_chart.py',
    )

    extract >> transform >> load >> chart
