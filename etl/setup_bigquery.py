from google.cloud import bigquery

def setup_bigquery():
    client = bigquery.Client()
    dataset_id = f"{client.project}.briefly_data"

    # Create dataset if it doesn't exist
    try:
        client.get_dataset(dataset_id)  # Make an API call.
        print(f"Dataset {dataset_id} already exists.")
    except Exception:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"Created dataset {dataset_id}")

    # Define table schema
    table_id = f"{dataset_id}.summaries"
    schema = [
        bigquery.SchemaField("url", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("title", "STRING"),
        bigquery.SchemaField("summary", "STRING"),
        bigquery.SchemaField("source", "STRING"),
        bigquery.SchemaField("published_at", "TIMESTAMP"),
        bigquery.SchemaField("summarized_at", "TIMESTAMP"),
    ]

    # Create table if it doesn't exist
    try:
        client.get_table(table_id)
        print(f"Table {table_id} already exists.")
    except Exception:
        table = bigquery.Table(table_id, schema=schema)
        client.create_table(table)
        print(f"Created table {table_id}")

if __name__ == "__main__":
    setup_bigquery()