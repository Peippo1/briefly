

from extract import extract_top_stories
from summarize import summarize_stories
from load import load_to_bigquery
import os

def main():
    print("🚀 Starting ETL pipeline...")

    # Extract
    print("📥 Extracting stories...")
    stories = extract_top_stories(10)
    if not stories:
        print("❌ No stories extracted. Exiting.")
        return

    # Summarize
    print("🧠 Summarizing stories...")
    summaries = summarize_stories(stories)
    if not summaries:
        print("❌ Summarization failed. Exiting.")
        return

    # Load to BigQuery
    print("📤 Loading to BigQuery...")
    dataset = os.getenv("BQ_DATASET", "briefly_data")
    table = os.getenv("BQ_TABLE", "summaries")
    load_to_bigquery(summaries, dataset=dataset, table=table)

    print("✅ Pipeline completed successfully.")

if __name__ == "__main__":
    main()