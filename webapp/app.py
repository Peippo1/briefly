import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from etl.summarize import summarize_stories
from etl.extract import extract_top_stories

def get_logo(domain):
    if domain:
        return f"https://logo.clearbit.com/{domain}"
    return "https://ui-avatars.com/api/?name=News&background=0D8ABC&color=fff"

st.set_page_config(page_title="📰 Briefly", layout="wide", page_icon="📰")

# Custom CSS for navbar styling
st.markdown("""
<style>
.navbar {
    background-color: #f0f2f6;
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
</style>
""", unsafe_allow_html=True)

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
        st.markdown("""
        <div class="navbar">
            <button id="feed_btn" class="{feed_class}">Feed</button>
            <button id="trending_btn" class="{trending_class}">Trending</button>
        </div>
        """.format(
            feed_class="selected" if st.session_state.page == "Feed" else "",
            trending_class="selected" if st.session_state.page == "Trending" else ""
        ), unsafe_allow_html=True)
    with cols[1]:
        theme = st.radio("Theme toggle", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1, horizontal=True, key="theme_radio", label_visibility="collapsed")

# Update session state based on radio and navbar button clicks via JS
# Since Streamlit does not natively support JS events on buttons,
# we handle theme toggle via radio and page via st.selectbox workaround below.

page = st.selectbox("Page select", ["Feed", "Trending"], index=0 if st.session_state.page == "Feed" else 1, key="page_select", label_visibility="collapsed")
st.session_state.page = page
st.session_state.theme = theme

# Apply theme CSS based on session_state.theme
if st.session_state.theme == "Dark":
    st.markdown("""
        <style>
        body {
            background-color: #0e1117;
            color: #fafafa;
        }
        .headline-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #ffffff;
        }
        .summary-block {
            font-size: 1rem;
            line-height: 1.6;
            color: #dcdcdc;
        }
        .stButton>button {
            background-color: #262730;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body {
            background-color: #ffffff;
            color: #000000;
        }
        .headline-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #111111;
        }
        .summary-block {
            font-size: 1rem;
            line-height: 1.6;
            color: #444444;
        }
        .stButton>button {
            background-color: #f0f0f0;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("📰 Briefly – AI News Summaries")
st.caption("Real-time headlines summarized using Gemini 1.5 Pro")

# Fetch and summarize data
with st.spinner("Fetching and summarizing top headlines..."):
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
    start_date, end_date = st.sidebar.date_input("Select date range", [min_date, max_date])

    st.sidebar.header("🌐 Source")
    all_sources = sorted(df["source"].dropna().unique())
    selected_sources = st.sidebar.multiselect("Select sources", all_sources, default=all_sources)

    # Apply filters
    df = df[(df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)]
    df = df[df["source"].isin(selected_sources)]

    st.markdown("---")

    for _, row in df.iterrows():
        st.markdown(f"📅 *{row['datetime'].strftime('%b %d, %Y %I:%M %p')}*", unsafe_allow_html=True)
        st.markdown(f"<div class='headline-title'>{row['title']}</div>", unsafe_allow_html=True)
        st.info(row["summary"])
        if row["url"]:
            domain = row["url"].split("/")[2]
            st.image(get_logo(domain), width=64)
            st.markdown(f"[🔗 Read more]({row['url']})")
        st.markdown("---")

elif st.session_state.page == "Trending":
    st.header("🔥 Trending Now")
    trending = df.sort_values(by="time", ascending=False).head(5)
    for _, row in trending.iterrows():
        st.markdown(f"📅 *{row['datetime'].strftime('%b %d, %Y %I:%M %p')}*", unsafe_allow_html=True)
        st.markdown(f"<div class='headline-title'>{row['title']}</div>", unsafe_allow_html=True)
        st.info(row["summary"])
        if row["url"]:
            domain = row["url"].split("/")[2]
            st.image(get_logo(domain), width=64)
            st.markdown(f"[🔗 Read more]({row['url']})")
        st.markdown("---")
