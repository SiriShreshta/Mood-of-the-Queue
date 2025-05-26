import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import json

# Page setup
st.set_page_config(page_title="Mood Logger", page_icon="🧠", layout="centered")
st_autorefresh(interval=30 * 1000, key="refresh")

# Google Sheets authentication using Streamlit secrets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_dict = json.loads(st.secrets["creds"])  # Replace creds.json with Streamlit secret
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Mood Log").sheet1

# App title
st.title("🧠 Mood of the Queue")
st.markdown("Capture and visualize how your team feels throughout the day.")

# Mood submission section
st.subheader("Log a Mood")
col1, col2 = st.columns(2)
with col1:
    mood = st.selectbox("How are things feeling?", ["😊", "😠", "😕", "🎉"])
with col2:
    note = st.text_input("Add a quick note (optional)")

if st.button("Submit Mood"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, mood, note])
    st.success("Mood logged successfully!")

# Mood chart section
st.subheader("📊 Mood Chart")

# Load and filter data
data = sheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    selected_date = st.date_input("Pick a date", datetime.today().date())
    filtered = df[df['Timestamp'].dt.date == selected_date]

    if not filtered.empty:
        mood_counts = filtered['Mood'].value_counts().reset_index()
        mood_counts.columns = ['Mood', 'Count']
        fig = px.bar(mood_counts, x='Mood', y='Count', color='Mood', title=f"Mood Summary for {selected_date}")
        st.plotly_chart(fig)
    else:
        st.info("No mood entries found for this date.")
else:
    st.info("No data available yet.")

# Footer
st.markdown("---")
st.caption("📊 Built by Siri Shreshta Reddy • Take-Home Assignment for Mochi Health")
