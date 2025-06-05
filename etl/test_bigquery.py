from google.cloud import bigquery
import os


def test_bigquery_connection():
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("GOOGLE_APPLICATION_CREDENTIALS is not set.")
    project_id = os.getenv("GCP_PROJECT")
    client = bigquery.Client(project=project_id) if project_id else bigquery.Client()
    project_id = client.project  # ensure we have the actual project used
    print(f"Using GCP Project: {project_id}")

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
