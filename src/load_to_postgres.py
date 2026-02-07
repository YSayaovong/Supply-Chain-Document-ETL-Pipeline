import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# ---------------------------
# Paths
# ---------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

MASKED_FILE = PROJECT_ROOT / "data" / "employee_data_masked.csv"

# ---------------------------
# Env vars
# ---------------------------
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_TABLE = os.getenv("PG_TABLE", "employees")

if not PG_DB or not PG_USER or not PG_PASS:
    raise ValueError("Missing required .env values: PG_DB, PG_USER, PG_PASS")

if not MASKED_FILE.exists():
    raise FileNotFoundError(
        f"Masked CSV not found: {MASKED_FILE}\n"
        "Run: python src\\extract.py then python src\\transform.py"
    )

def sanitize(col: str) -> str:
    # safe postgres identifiers: lower, underscores
    col = col.strip().lower()
    col = col.replace(" ", "_").replace("-", "_")
    return col

def load_data():
    # Read CSV header
    header_line = MASKED_FILE.read_text(encoding="utf-8").splitlines()[0]
    raw_cols = [c.strip() for c in header_line.split(",")]
    cols = [sanitize(c) for c in raw_cols]

    # Build SQL
    col_defs = ",\n    ".join([f"{c} TEXT" for c in cols])
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS {PG_TABLE} (
        {col_defs}
    );
    """

    truncate_sql = f"TRUNCATE TABLE {PG_TABLE};"

    col_list = ", ".join(cols)
    copy_sql = f"""
    COPY {PG_TABLE} ({col_list})
    FROM STDIN WITH (FORMAT CSV, HEADER TRUE);
    """

    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASS,
    )

    try:
        with conn:
            with conn.cursor() as cur:
                # Create table based on CSV header
                cur.execute(create_sql)
                cur.execute(truncate_sql)

                # Load
                with MASKED_FILE.open("r", encoding="utf-8") as f:
                    cur.copy_expert(copy_sql, f)

        print(f"[load] Loaded {MASKED_FILE} into table: {PG_TABLE}")
        print(f"[load] Columns: {cols}")

    finally:
        conn.close()

if __name__ == "__main__":
    load_data()
