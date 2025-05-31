
![Python CI](https://github.com/Peippo1/briefly/actions/workflows/blank.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)

![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit)
![Dockerized](https://img.shields.io/badge/Dockerized-Yes-blue?logo=docker)
![Powered by Databricks](https://img.shields.io/badge/Powered%20by-Databricks-orange?logo=databricks)
![Runs on GCP](https://img.shields.io/badge/Runs%20on-Google%20Cloud-blue?logo=googlecloud)


# 📰 Briefly

**Briefly** is a lightweight, AI-powered ETL pipeline that pulls trending news headlines, summarizes them using Google's Gemini API, and displays them in a clean web app interface. It's built with Databricks, Python, and Streamlit — ideal for showcasing real-time NLP + data engineering skills.

## 🚀 Features

- Extract top news stories from Hacker News
- Summarize headlines using Gemini 1.5 Pro
- Display summaries in a dynamic Streamlit app
- Top navigation bar with Feed and Trending views
- Light/Dark theme toggle in the header
- Live date range and source filtering in the sidebar
- Preview logos for each article (with fallback)
- Optional support for Delta Tables, BigQuery, or CSV export
- Free-tier compatible (Google Gemini 1.5)

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
# Create and activate your virtual environment (if needed)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Summarize latest headlines
python etl/summarize.py

# Launch the frontend dashboard
streamlit run webapp/app.py
```

## 📜 License

MIT — free to use, extend, and showcase.