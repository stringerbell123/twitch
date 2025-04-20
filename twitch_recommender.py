
import streamlit as st
import pandas as pd
from datetime import datetime

# App setup
st.set_page_config(
    page_title="Twitch Stream Recommender",
    page_icon="🎮",
    layout="wide"
)

# Load data
try:
    df = pd.read_csv("streams.csv")
    df['Started'] = pd.to_datetime(df['Started'])
except Exception as e:
    st.error(f"Data load error: {e}")
    st.stop()

# Sidebar filters
with st.sidebar:
    st.title("Filters")
    selected_games = st.multiselect(
        "Choose categories:",
        options=sorted(df['Game'].unique()),
        default=["Just Chatting"]
    )
    min_viewers = st.slider("Minimum viewers", 0, 10000, 500)

# Display streams
st.title("🎮 Recommended Twitch Streams")
filtered = df[df['Game'].isin(selected_games) & (df['Viewers'] >= min_viewers)]

for _, row in filtered.iterrows():
    with st.container(border=True):
        st.markdown(f"**{row['Streamer']}** playing *{row['Game']}*")
        st.caption(f"👀 {row['Viewers']} viewers | 🕒 {row['Started'].strftime('%H:%M')}")
        st.write(row['Title'])
        st.link_button("Watch Live", f"https://twitch.tv/{row['Streamer']}")
