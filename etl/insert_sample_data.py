from google.cloud import bigquery
from datetime import datetime


def insert_sample_data():
    client = bigquery.Client()
    table_id = f"{client.project}.briefly_data.summaries"

    rows_to_insert = [
        {
            "url": "https://news.ycombinator.com/item?id=123456",
            "title": "Sample Hacker News Article",
            "summary": "This article discusses recent advancements in AI and their implications.",
            "source": "Hacker News",
            "published_at": datetime(2024, 12, 15, 12, 0, 0).isoformat(),
            "summarized_at": datetime.utcnow().isoformat(),
        },
    ]

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows:", errors)

    # Query to confirm insertion
    query = f"""
    SELECT url, title, summarized_at
    FROM `{table_id}`
    ORDER BY summarized_at DESC
    LIMIT 5
    """

    query_job = client.query(query)
    print("Recent entries in summaries table:")
    for row in query_job:
        print(f"- {row['title']} ({row['url']}) at {row['summarized_at']}")


if __name__ == "__main__":
    insert_sample_data()
