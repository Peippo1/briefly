


# --------------------------------------------------
# Output the dataset ID
# --------------------------------------------------
output "bigquery_dataset_id" {
  description = "The ID of the BigQuery dataset"
  value       = google_bigquery_dataset.briefly_dataset.dataset_id
}

# --------------------------------------------------
# Output the full table ID
# --------------------------------------------------
output "bigquery_table_id" {
  description = "The full ID of the BigQuery summaries table"
  value       = google_bigquery_table.summaries_table.id
}

# --------------------------------------------------
# Output the service account email
# --------------------------------------------------
output "etl_service_account_email" {
  description = "The email address of the ETL service account"
  value       = google_service_account.etl_service_account.email
}