import sys
import os
import json

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

import streamlit as st

# Use Streamlit secrets in deployed environment
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
if "GOOGLE_APPLICATION_CREDENTIALS_JSON" in st.secrets:
    credentials = st.secrets["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gcp-creds.json"
    with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], "w") as f:
        if isinstance(credentials, str):
            creds_dict = json.loads(credentials)
        else:
            creds_dict = dict(credentials)
        json.dump(creds_dict, f)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from etl.summarize import summarize_stories
from etl.extract import extract_top_stories


def get_logo(domain):
    if domain:
        return f"https://logo.clearbit.com/{domain}"
    return "https://ui-avatars.com/api/?name=News&background=0D8ABC&color=fff"


# Check for required API key
if "GEMINI_API_KEY" not in os.environ:
    st.error("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
    st.stop()


st.set_page_config(page_title="📰 Briefly", layout="wide", page_icon="📰")

# Custom CSS for navbar styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

.navbar {
    background-color: #80D8C3;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}
.navbar button {
    background-color: transparent;
    border: none;
    font-size: 1.1rem;
    margin: 0 10px;
    cursor: pointer;
}
.navbar button.selected {
    font-weight: bold;
    text-decoration: underline;
}
.theme-toggle {
    font-size: 1rem;
}
html, body, .main, section.main, div.block-container {
    background-color: #F3F3E0 !important;
    color: #F5F5F5 !important;
    font-family: 'Roboto', sans-serif !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state for page and theme
if "page" not in st.session_state:
    st.session_state.page = "Feed"
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# Navbar container
nav_container = st.container()

with nav_container:
    cols = st.columns([3, 1])
    with cols[0]:
        st.markdown(
            """
        <div class="navbar">
            <button id="feed_btn" class="{feed_class}">Feed</button>
            <button id="trending_btn" class="{trending_class}">Trending</button>
        </div>
        """.format(
                feed_class="selected" if st.session_state.page == "Feed" else "",
                trending_class=(
                    "selected" if st.session_state.page == "Trending" else ""
                ),
            ),
            unsafe_allow_html=True,
        )
    with cols[1]:
        theme = st.radio(
            "Theme toggle",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "Light" else 1,
            horizontal=True,
            key="theme_radio",
            label_visibility="collapsed",
        )

# Update session state based on radio and navbar button clicks via JS
# Since Streamlit does not natively support JS events on buttons,
# we handle theme toggle via radio and page via st.selectbox workaround below.

page = st.selectbox(
    "Page select",
    ["Feed", "Trending"],
    index=0 if st.session_state.page == "Feed" else 1,
    key="page_select",
    label_visibility="collapsed",
)
st.session_state.page = page
st.session_state.theme = theme

# Apply theme CSS based on session_state.theme
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

        html, body, .main, section.main, div.block-container {
            background-color: #F3F3E0 !important;
            color: #F5F5F5 !important;
            font-family: 'Roboto', sans-serif !important;
        }
        .headline-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #F5F5F5;
        }
        .summary-block {
            font-size: 1rem;
            line-height: 1.6;
            color: #F5F5F5;
        }
        .stButton>button {
            background-color: #262730;
            color: white;
        }
        .swiper-slide {
          background: #27548A;
          border-radius: 6px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          padding: 20px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

        html, body, .main, section.main, div.block-container {
            background-color: #F3F3E0 !important;
            color: #F5F5F5 !important;
            font-family: 'Roboto', sans-serif !important;
        }
        .headline-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #F5F5F5;
        }
        .summary-block {
            font-size: 1rem;
            line-height: 1.6;
            color: #F5F5F5;
        }
        .stButton>button {
            background-color: #f0f0f0;
            color: black;
        }
        .swiper-slide {
          background: #27548A;
          border-radius: 6px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          padding: 20px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

st.markdown('<h1 style="color:#183B4E;">📰 Briefly – AI News Summaries</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#183B4E; font-size: 1rem;">Real-time headlines summarized using Gemini 1.5 Pro</p>', unsafe_allow_html=True)

# Fetch and summarize data
with st.spinner("🌀 Fetching and summarizing top headlines..."):
    st.markdown(
        "<style>.stSpinner span { color: #183B4E !important; }</style>",
        unsafe_allow_html=True,
    )
    stories = extract_top_stories(10)
    summarized = summarize_stories(stories)
    df = pd.DataFrame(summarized)

# Convert time to datetime and extract source
df["datetime"] = pd.to_datetime(df["time"], unit="s")
df["source"] = df["url"].apply(lambda x: None if pd.isna(x) else x.split("/")[2])

if st.session_state.page == "Feed":
    # Sidebar filters
    st.sidebar.header("🗓️ Date range")
    min_date = df["datetime"].min().date()
    max_date = df["datetime"].max().date()
    start_date, end_date = st.sidebar.date_input(
        "Select date range", [min_date, max_date]
    )

    st.sidebar.header("🌐 Source")
    all_sources = sorted(df["source"].dropna().unique())
    selected_sources = st.sidebar.multiselect(
        "Select sources", all_sources, default=all_sources
    )

    # Apply filters
    df = df[
        (df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)
    ]
    df = df[df["source"].isin(selected_sources)]

    st.markdown("---")

    for _, row in df.iterrows():
        with st.container():
            domain = None
            if row["url"]:
                domain = row["url"].split("/")[2]
            bg_color = "#27548A"
            st.markdown(
                f"""
                <div style="border-radius:6px; padding:15px; margin:10px 0; background-color:#27548A; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="display:flex; align-items:center;">
                        <img src="{get_logo(domain)}" width="48" style="margin-right:10px;" />
                        <div>
                            <div style="font-size: 0.9rem; color: #666;">📅 {row['datetime'].strftime('%b %d, %Y %I:%M %p')}</div>
                            <h4 style="margin: 0;">{row['title']}</h4>
                        </div>
                    </div>
                    <p style="margin-top:10px;">{row['summary']}</p>
                    <a href="{row['url']}" target="_blank" style="color:#1a73e8;">🔗 Read more</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

elif st.session_state.page == "Trending":
    from streamlit.components.v1 import html

    st.header("🔥 Trending Now")
    trending = df.sort_values(by="time", ascending=False).head(5)

    carousel_html = """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper/swiper-bundle.min.css"/>
    <script src="https://cdn.jsdelivr.net/npm/swiper/swiper-bundle.min.js"></script>
    <style>
    .swiper-container {{
      width: 100%;
      padding-top: 20px;
      padding-bottom: 40px;
    }}
    .swiper-slide {{
      background: #27548A;
      border-radius: 6px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    </style>
    <div class="swiper-container">
      <div class="swiper-wrapper">
        {slides}
      </div>
      <div class="swiper-pagination"></div>
    </div>
    <script>
      new Swiper('.swiper-container', {{
        loop: true,
        autoplay: {{
          delay: 5000,
        }},
        pagination: {{
          el: '.swiper-pagination',
        }},
      }});
    </script>
    """

    slides_html = ""
    for _, row in trending.iterrows():
        slides_html += f"""
        <div class="swiper-slide">
          <img src="{get_logo(row['source'])}" style="width:64px;height:auto;margin-bottom:10px;" />
          <h4>{row["title"]}</h4>
          <p>{row["summary"]}</p>
          <a href="{row["url"]}" target="_blank">🔗 Read more</a>
        </div>
        """

    html(carousel_html.format(slides=slides_html), height=400)


# Optional: Warn if no articles found
if df.empty:
    st.warning("No news items found for the selected filters.")
