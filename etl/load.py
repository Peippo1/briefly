import pandas as pd
from google.cloud import bigquery
import os

def load_to_bigquery(data: list, dataset: str, table: str, mode: str = "WRITE_APPEND"):
    """Loads summarized news stories to BigQuery"""
    if not data:
        print("⚠️ No data to load.")
        return

    df = pd.DataFrame(data)
    project = os.getenv("GCP_PROJECT")
    client = bigquery.Client(project=project) if project else bigquery.Client()

    table_id = f"{client.project}.{dataset}.{table}"

    job_config = bigquery.LoadJobConfig(write_disposition=mode)
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"✅ Loaded {len(df)} rows to {table_id} using mode '{mode}'")