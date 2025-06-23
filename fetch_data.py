import requests
import pandas as pd
import os
from dotenv import load_dotenv

# API key from .env
load_dotenv()
API_KEY = os.getenv("DATA_GOV_API_KEY")

# Resource Id(from data.gov.in)
RESOURCE_ID = "35be999b-0208-4354-b557-f6ca9a5355de"
URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"

# Output path
os.makedirs("data", exist_ok=True)
CSV_OUT = "data/crop_data_raw.csv"

def fetch_data(limit=50000):
    print("[INFO] Fetching data...")
    params = {
        "api-key": API_KEY,
        "format":"json",
        "limit": limit
    }
    res = requests.get(URL, params=params)
    res.raise_for_status()
    records = res.json().get("records", [])
    df = pd.DataFrame(records)
    df.to_csv(CSV_OUT, index=False)
    print(f"[DONE] Pulled {len(df)} records > {CSV_OUT}")
    return df

if __name__=="__main__":
    fetch_data()