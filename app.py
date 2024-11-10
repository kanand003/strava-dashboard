# app.py
import streamlit as st
import requests
import pandas as pd

# Function to fetch Strava runs
def fetch_strava_runs(access_token):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Streamlit app
st.title("My Strava Runs")

# Replace with your actual access token
access_token = "750483ba414660a6f1008cd1a739716b24edb67d"

# Fetch and display runs
try:
    runs = fetch_strava_runs(access_token)
    runs_df = pd.DataFrame(runs)

    # Display the DataFrame to check its structure
    st.write("DataFrame Structure:")
    st.write(runs_df.head())
    st.write("Column Names:")
    st.write(runs_df.columns)

    # Convert 'start_date' to datetime
    runs_df['start_date'] = pd.to_datetime(runs_df['start_date'], errors='coerce')

    # Check for null values in 'start_date'
    if runs_df['start_date'].isnull().any():
        st.warning("Some start dates could not be parsed. Check the data.")

    # Filters
    activity_types = ['Run', 'Ride', 'Swim']
    selected_type = st.selectbox("Select Activity Type", activity_types)
    start_date = st.date_input("Start Date", value=pd.to_datetime('2022-01-01').date())
    end_date = st.date_input("End Date", value=pd.to_datetime('today').date())

    # Filter runs
    filtered_runs = runs_df[
        (runs_df['type'] == selected_type) &
        (runs_df['start_date'] >= start_date) &
        (runs_df['start_date'] <= end_date)
    ]
    
    st.write(filtered_runs[['name', 'distance', 'moving_time', 'start_date']])

except Exception as e:
    st.error(f"Error fetching runs: {e}")
