# etl/summarize.py

import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print("Using API Key:", api_key[:8] + "...")

if not api_key:
    raise ValueError("GEMINI_API_KEY not set in .env")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

def summarize_headline(headline: str) -> str:
    try:
        prompt = f"Summarize this news headline in one sentence: '{headline}'"
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        print(f"Error summarizing: {headline[:60]}... – {e}")
        return "Summary unavailable"

def summarize_stories(stories: list, delay_seconds=1) -> list:
    summarized = []
    for story in stories:
        title = story.get("title")
        summary = summarize_headline(title)
        story["summary"] = summary
        summarized.append(story)
        time.sleep(delay_seconds)  # 🧘 Throttle to avoid hitting rate limits
    return summarized

if __name__ == "__main__":
    from extract import extract_top_stories
    from pprint import pprint

    top_stories = extract_top_stories(5)
    summaries = summarize_stories(top_stories)
    pprint(summaries)