#!/usr/bin/env python3
"""
Script to read FAR-Trans CSV files and insert all rows into PostgreSQL via API.
"""

import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from tqdm import tqdm


# Configuration
API_BASE_URL = "http://localhost:8000"
API_ENDPOINT_TEMPLATE = f"{API_BASE_URL}/data/training/{{dataset}}"

# CSV file to dataset mapping
CSV_TO_DATASET = {
    "customer_information.csv": "customer_information",
    "asset_information.csv": "asset_information",
    "markets.csv": "markets",
    "close_prices.csv": "close_prices",
    "limit_prices.csv": "limit_prices",
    "transactions.csv": "transactions",
}


def clean_value(value: str) -> Optional[Any]:
    """Convert CSV string values to appropriate types."""
    if value is None or value == "" or value.strip() == "":
        return None
    value = value.strip()
    # Try to convert to float if it looks like a number
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def convert_row_to_dict(row: Dict[str, str], dataset: str) -> Dict[str, Any]:
    """Convert CSV row to API payload format.

    Keep identifier-style fields as strings to avoid stripping leading zeros or type mismatches.
    Only numeric-cast known numeric fields.
    """
    id_fields = {"ISIN", "customerID", "transactionID", "marketID", "exchangeID"}
    numeric_fields = {"closePrice", "totalValue", "units", "priceMinDate", "priceMaxDate", "profitability"}

    cleaned_row: Dict[str, Any] = {}
    for key, value in row.items():
        if value == "":
            cleaned_row[key] = None
            continue

        if key in id_fields:
            cleaned_row[key] = value.strip()
            continue

        if key in numeric_fields:
            cleaned_row[key] = clean_value(value)
            continue

        # Dates and other strings are passed through as-is; server validates/parses
        cleaned_row[key] = value.strip()

    return cleaned_row


def insert_row(dataset: str, payload: Dict[str, Any]) -> bool:
    """Make API call to insert a single row."""
    url = API_ENDPOINT_TEMPLATE.format(dataset=dataset)
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return True
        else:
            print(f"\nError inserting row: {response.status_code} - {response.text}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"\nRequest error: {e}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        return False


def insert_batch(dataset: str, payload_list: list[Dict[str, Any]], batch_size: int = 10000) -> tuple[int, int]:
    """Make API call to insert a batch of rows."""
    url = f"{API_BASE_URL}/data/training/{dataset}/batch"
    success_count = 0
    error_count = 0
    
    total_batches = (len(payload_list) + batch_size - 1) // batch_size
    
    # Process in chunks to avoid overwhelming the API
    for i in tqdm(range(0, len(payload_list), batch_size), desc="Inserting batches", total=total_batches, unit="batch"):
        batch = payload_list[i:i + batch_size]
        try:
            response = requests.post(url, json=batch, timeout=300)
            if response.status_code == 200:
                result = response.json()
                success_count += result.get("rows_inserted", len(batch))
            else:
                print(f"\nError inserting batch {i//batch_size + 1}: {response.status_code} - {response.text}")
                error_count += len(batch)
        except requests.exceptions.RequestException as e:
            print(f"\nRequest error for batch {i//batch_size + 1}: {e}")
            error_count += len(batch)
    
    return success_count, error_count


def process_csv_file(csv_path: Path, dataset: str, use_batch: bool = False) -> tuple[int, int]:
    """Process a single CSV file and insert all rows.

    If parallel > 1 and dataset is 'close_prices', rows will be inserted concurrently.
    If use_batch is True, uses batch insert endpoint (for customer_information and limit_prices).
    """
    print(f"\nProcessing {csv_path.name} -> {dataset}")
    
    success_count = 0
    error_count = 0
    
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            if use_batch and dataset in ["customer_information", "close_prices", "transactions"]:
                # Convert all rows to payloads
                payloads = []
                for row in tqdm(rows, desc=f"Preparing {dataset}", unit="rows"):
                    payload = convert_row_to_dict(row, dataset)
                    payloads.append(payload)
                
                # Insert in batches
                print(f"Inserting {len(payloads)} rows in batches...")
                success, errors = insert_batch(dataset, payloads)
                success_count = success
                error_count = errors
            else:
                # Use tqdm for progress bar
                for row in tqdm(rows, desc=f"Inserting {dataset}", unit="rows"):
                    payload = convert_row_to_dict(row, dataset)
                    if insert_row(dataset, payload):
                        success_count += 1
                    else:
                        error_count += 1
                    
    except FileNotFoundError:
        print(f"Error: File {csv_path} not found")
        return 0, 0
    except Exception as e:
        print(f"Error processing {csv_path}: {e}")
        return success_count, error_count
    
    return success_count, error_count


def main():
    """Main function to process all CSV files."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    print(f"FAR-Trans Data Ingestion Script")
    print(f"API URL: {API_BASE_URL}")
    print(f"Working directory: {script_dir}")
    print("-" * 50)
    
    # Check if API is accessible
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if health_response.status_code != 200:
            print(f"Warning: API health check failed (status {health_response.status_code})")
            print("Continuing anyway...")
    except requests.exceptions.RequestException as e:
        print(f"Warning: Cannot connect to API at {API_BASE_URL}")
        print(f"Error: {e}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != "y":
            sys.exit(1)
    
    total_success = 0
    total_errors = 0
    
    # Process each CSV file
    for csv_filename, dataset in CSV_TO_DATASET.items():
        csv_path = script_dir / csv_filename
        
        if not csv_path.exists():
            print(f"Warning: {csv_filename} not found, skipping...")
            continue
        
        if dataset in ("customer_information", "close_prices", "transactions"):
            # Use batch insert for selected datasets
            success, errors = process_csv_file(csv_path, dataset, use_batch=True)
        total_success += success
        total_errors += errors
        
        print(f"  ✓ Success: {success}, Errors: {errors}")
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total rows inserted successfully: {total_success}")
    print(f"Total errors: {total_errors}")
    print(f"Total rows processed: {total_success + total_errors}")
    
    if total_errors > 0:
        print(f"\n⚠️  {total_errors} rows failed to insert. Check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ All rows inserted successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()

