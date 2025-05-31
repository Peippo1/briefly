

# 📰 Briefly

**Briefly** is a lightweight, AI-powered ETL pipeline that pulls trending news headlines, summarizes them using Google's Gemini API, and displays them in a clean web app interface. It's built with Databricks, Python, and Streamlit — ideal for showcasing real-time NLP + data engineering skills.

## 🚀 Features

- Extract top news stories from Hacker News
- Use Gemini 1.5 Pro for headline summarization
- Clean and structure data using PySpark and Pandas
- Display output in a Streamlit app
- Optional support for Delta Tables, BigQuery, or CSV export
- Free-tier compatible

## 🧱 Tech Stack

- **Python** (ETL scripts)
- **Databricks** (processing environment)
- **Gemini API** (summarization)
- **Streamlit** (web UI)
- **Terraform** (infra-as-code, optional)
- **Docker** (optional for app deployment)

## 📂 Project Structure

```
briefly/
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── summarize.py
│   └── load.py
├── webapp/
│   └── app.py
├── notebooks/
│   └── databricks_etl.ipynb
├── terraform/
│   └── main.tf
├── requirements.txt
└── README.md
```

## 🔑 Environment Setup

1. Clone the repo
2. Create a `.env` file:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## 🧪 Run Locally

```bash
# Summarize latest headlines
python etl/summarize.py

# Run the frontend
streamlit run webapp/app.py
```

## 📜 License

MIT — free to use, extend, and showcase.