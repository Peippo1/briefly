import pandas as pd
from google.cloud import bigquery
import os
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

def load_to_bigquery(data: list, dataset: str, table: str, mode: str = "WRITE_APPEND"):
    """Loads summarized news stories to BigQuery with deduplication and retry logic"""
    
    if not data:
        logging.warning("No data to load.")
        return

    allowed_fields = {"url", "title", "summary", "source", "published_at", "summarized_at"}

    project = os.getenv("GCP_PROJECT")
    client = bigquery.Client(project=project) if project else bigquery.Client()

    table_id = f"{client.project}.{dataset}.{table}"

    query = f"SELECT url FROM `{table_id}`"
    existing_urls = set()
    try:
        query_job = client.query(query)
        existing_urls = {row.url for row in query_job}
    except Exception as e:
        logging.warning(f"Could not retrieve existing URLs from BigQuery. Proceeding without de-duplication. Error: {e}")

    cleaned_data = [
        {k: v for k, v in row.items() if k in allowed_fields}
        for row in data
        if row.get("url") not in existing_urls
    ]

    if not cleaned_data:
        logging.info("No new unique rows to load. All entries already exist in BigQuery.")
        return

    df = pd.DataFrame(cleaned_data)
    job_config = bigquery.LoadJobConfig(write_disposition=mode)

    # Retry logic
    for attempt in range(3):
        try:
            job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
            job.result()  # Wait for completion
            logging.info(f"Loaded {len(df)} rows to {table_id} using mode '{mode}'")
            break
        except Exception as load_error:
            logging.error(f"Attempt {attempt + 1} failed to load data to BigQuery: {load_error}")
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                logging.critical("All retry attempts failed.")