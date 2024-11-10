import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch Strava runs
def fetch_strava_runs(access_token):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Streamlit app
st.title("My Strava Runs")

# Replace with your actual access token
access_token = "YOUR_ACCESS_TOKEN"  # Replace with your access token

# Fetch and display runs
try:
    runs = fetch_strava_runs(access_token)
    runs_df = pd.DataFrame(runs)

    # Filters
    activity_types = ['Run', 'Ride', 'Swim']
    selected_type = st.selectbox("Select Activity Type", activity_types)
    start_date = st.date_input("Start Date", value=pd.to_datetime('2022-01-01'))
    end_date = st.date_input("End Date", value=pd.to_datetime('today'))

    # Filter runs
    filtered_runs = runs_df[(runs_df['type'] == selected_type) & 
                             (pd.to_datetime(runs_df['start_date']) >= start_date) & 
                             (pd.to_datetime(runs_df['start_date']) <= end_date)]
    
    st.write(filtered_runs[['name', 'distance', 'moving_time', 'start_date']])

    # Metrics
    if not filtered_runs.empty:
        total_distance = filtered_runs['distance'].sum()
        total_time = filtered_runs['moving_time'].sum() / 60  # Convert to minutes
        st.write(f"Total Distance: {total_distance} meters")
        st.write(f"Total Time: {total_time:.2f} minutes")

        # Plot distance over time
        filtered_runs['start_date'] = pd.to_datetime(filtered_runs['start_date'])
        plt.figure(figsize=(10, 5))
        plt.plot(filtered_runs['start_date'], filtered_runs['distance'], marker='o')
        plt.title('Distance Over Time')
        plt.xlabel('Date')
        plt.ylabel('Distance (meters)')
        plt.xticks(rotation=45)
        st.pyplot(plt)

except Exception as e:
    st.error(f"Error fetching runs: {e}")