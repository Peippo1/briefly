# --------------------------------------------------
# Project ID for your GCP environment
# --------------------------------------------------
variable "project_id" {
  description = "The GCP project ID to use for resource creation"
  type        = string
}

# --------------------------------------------------
# Region for BigQuery resources
# --------------------------------------------------
variable "region" {
  description = "The GCP region to deploy resources in (e.g., US or EU)"
  type        = string
  default     = "US"
}
