import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

OUT_DIR = PROJECT_ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)
OUT_FILE = OUT_DIR / "employees_by_department.png"

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_TABLE = os.getenv("PG_TABLE", "employees")

# We will try common column names in order:
DEPT_CANDIDATES = ["department", "dept", "team", "org"]

def generate_chart():
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASS,
    )

    try:
        with conn.cursor() as cur:
            # Find which dept column exists
            cur.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s;
                """,
                (PG_TABLE,)
            )
            cols = [r[0] for r in cur.fetchall()]

            dept_col = None
            for c in DEPT_CANDIDATES:
                if c in cols:
                    dept_col = c
                    break

            if not dept_col:
                raise ValueError(
                    f"No department-like column found in '{PG_TABLE}'. "
                    f"Columns are: {cols}"
                )

            query = f"""
            SELECT {dept_col} AS department, COUNT(*) AS employee_count
            FROM {PG_TABLE}
            GROUP BY {dept_col}
            ORDER BY employee_count DESC;
            """

            cur.execute(query)
            rows = cur.fetchall()

    finally:
        conn.close()

    departments = [r[0] for r in rows]
    counts = [r[1] for r in rows]

    plt.figure(figsize=(9, 4))
    plt.bar(departments, counts)
    plt.xticks(rotation=45, ha="right")
    plt.title("Employees by Department")
    plt.xlabel("Department")
    plt.ylabel("Employee Count")
    plt.tight_layout()
    plt.savefig(OUT_FILE, dpi=200)

    print(f"[chart] Saved: {OUT_FILE}")

if __name__ == "__main__":
    generate_chart()
