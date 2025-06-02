from google.cloud import bigquery
import os

def test_bigquery_connection():
    project_id = os.getenv('GCP_PROJECT')
    if not project_id:
        print("GCP_PROJECT environment variable is not set.")
        return

    client = bigquery.Client(project=project_id)

    try:
        datasets = list(client.list_datasets())
        if datasets:
            print(f"Datasets in project {project_id}:")
            for dataset in datasets:
                print(f"- {dataset.dataset_id}")
        else:
            print(f"No datasets found in project {project_id}.")
    except Exception as e:
        print(f"Failed to connect to BigQuery: {e}")

if __name__ == "__main__":
    test_bigquery_connection()