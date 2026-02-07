import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

IN_FILE = DATA_DIR / "employee_data.csv"
OUT_FILE = DATA_DIR / "employee_data_masked.csv"

def mask_email(email):
    return email.split("@")[0][:2] + "***@***"

def transform():
    df = pd.read_csv(IN_FILE)
    df["email"] = df["email"].apply(mask_email)

    df.to_csv(OUT_FILE, index=False)
    print(f"[transform] Wrote masked file: {OUT_FILE}")

if __name__ == "__main__":
    transform()
