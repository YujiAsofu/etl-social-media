import os
import json
import requests
import pandas as pd
from typing import Dict
from pathlib import Path

BASE_URL = "https://jsonplaceholder.typicode.com"

ENDPOINTS = {
    "users": "users",
    "posts": "posts",
    "comments": "comments",
    "tasks": "todos",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

def extract_endpoint(endpoint: str) -> list:
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, timeout=10)

    response.raise_for_status()

    return response.json()


def save_raw_data(data: list, filename: str) -> None:
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    file_path = os.path.join(RAW_DATA_DIR, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def extract() -> Dict[str, pd.DataFrame]:
    extracted_data = {}

    for name, endpoint in ENDPOINTS.items():
        data = extract_endpoint(endpoint)

        save_raw_data(data, f"{name}.json")

        extracted_data[name] = pd.DataFrame(data)

    return extracted_data

extract()