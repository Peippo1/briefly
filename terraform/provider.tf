# --------------------------------------------------
# Terraform configuration block
# --------------------------------------------------
# Specifies the required provider (Google Cloud) and version constraints
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0" # Use version 5.x of the Google provider
    }
  }

  # Specifies the minimum Terraform CLI version required
  required_version = ">= 1.3"
}


# --------------------------------------------------
# Google Cloud provider block
# --------------------------------------------------
# Configures the Google provider using variables for project and region
provider "google" {
  project = var.project_id
  region  = var.region
}
