import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

OUT_FILE = DATA_DIR / "employee_data.csv"

def extract():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["A", "B", "C"],
        "department": ["IT", "HR", "Finance"],
        "salary": [70000, 65000, 60000],
        "email": ["a@example.com", "b@example.com", "c@example.com"]
    })

    df.to_csv(OUT_FILE, index=False)
    print(f"[extract] Wrote: {OUT_FILE}")

if __name__ == "__main__":
    extract()
