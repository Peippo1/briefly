


# --------------------------------------------------
# Create a BigQuery Dataset
# --------------------------------------------------
# This resource creates a new BigQuery dataset named "briefly_data".
# The dataset will be used to store tables related to the Briefly project.
resource "google_bigquery_dataset" "briefly_dataset" {
  dataset_id    = "briefly_data"
  friendly_name = "Briefly Dataset"
  description   = "Dataset for storing summarised article data"
  location      = var.region
}

# --------------------------------------------------
# Create a BigQuery Table for summaries
# --------------------------------------------------
# This resource creates a table named "summaries" within the "briefly_data" dataset.
# The schema defines columns for URL, title, summary, source, published time, and summarized time.
resource "google_bigquery_table" "summaries_table" {
  dataset_id = google_bigquery_dataset.briefly_dataset.dataset_id
  table_id   = "summaries"

  # The schema is defined as a JSON-encoded array of column definitions.
  schema = jsonencode([
    {
      name = "url"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "title"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "summary"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "source"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "published_at"
      type = "TIMESTAMP"
      mode = "NULLABLE"
    },
    {
      name = "summarized_at"
      type = "TIMESTAMP"
      mode = "NULLABLE"
    }
  ])

  # Allows the table to be deleted without protection.
  deletion_protection = false
}

# --------------------------------------------------
# Create a service account for the ETL pipeline
# --------------------------------------------------
# This resource creates a service account to be used by the ETL (Extract, Transform, Load) pipeline.
# The service account will be granted permissions to access BigQuery resources.
resource "google_service_account" "etl_service_account" {
  account_id   = "briefly-etl"
  display_name = "ETL service account for Briefly pipeline"
}

# --------------------------------------------------
# Grant BigQuery User role to the service account
# --------------------------------------------------
# This resource assigns the BigQuery User role to the ETL service account.
# This allows the service account to run queries and manage tables in BigQuery.
resource "google_project_iam_member" "etl_bigquery_access" {
  project = var.project_id
  role    = "roles/bigquery.user"
  member  = "serviceAccount:${google_service_account.etl_service_account.email}"
}