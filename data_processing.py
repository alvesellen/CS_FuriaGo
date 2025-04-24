import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

def save_fan_data(fan_data):
    """Save the fan data to the session state and to a JSON file."""
    # Convert to DataFrame for a single row
    fan_df = pd.DataFrame([fan_data])
    
    # Update session state
    if 'fan_data' not in st.session_state or st.session_state.fan_data.empty:
        st.session_state.fan_data = fan_df
    else:
        st.session_state.fan_data = pd.concat([st.session_state.fan_data, fan_df], ignore_index=True)
    
    # Save to JSON file
    try:
        # Convert DataFrame to list of dictionaries
        data_list = st.session_state.fan_data.to_dict('records')
        
        # Convert timestamp objects to strings for JSON serialization
        for item in data_list:
            if 'timestamp' in item and isinstance(item['timestamp'], pd.Timestamp):
                item['timestamp'] = item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        with open('fan_data.json', 'w') as f:
            json.dump(data_list, f, indent=4)
    except Exception as e:
        st.error(f"Error saving data: {e}")

def load_fan_data():
    """Load fan data from the JSON file."""
    try:
        if os.path.exists('fan_data.json'):
            with open('fan_data.json', 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            
            # Convert timestamp strings back to datetime
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def get_social_media_data():
    """
    In a real application, this would fetch data from social media APIs.
    For this example, we'll return a placeholder DataFrame with simulated data.
    """
    # Note: In a real application, this would be replaced with actual API calls
    if 'social_media_data' in st.session_state and not st.session_state.social_media_data.empty:
        return st.session_state.social_media_data
    else:
        # Return empty DataFrame since we don't want to generate mock data
        return pd.DataFrame()

def process_engagement_data(fan_data):
    """Process fan engagement data for analytics."""
    if fan_data.empty:
        return pd.DataFrame()
    
    # Process the engagement_type which is stored as a list
    engagement_counts = {}
    for _, row in fan_data.iterrows():
        if isinstance(row.get('engagement_type'), list):
            for engagement in row['engagement_type']:
                engagement_counts[engagement] = engagement_counts.get(engagement, 0) + 1
    
    # Convert to DataFrame
    engagement_df = pd.DataFrame({
        'engagement_type': list(engagement_counts.keys()),
        'count': list(engagement_counts.values())
    })
    
    return engagement_df if not engagement_df.empty else pd.DataFrame()

def export_data_to_csv(data, filename):
    """Export DataFrame to CSV."""
    try:
        if not data.empty:
            data.to_csv(filename, index=False)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error exporting data: {e}")
        return False

def export_data_to_json(data, filename):
    """Export DataFrame to JSON."""
    try:
        if not data.empty:
            # Convert timestamp objects to strings for JSON serialization
            data_copy = data.copy()
            if 'timestamp' in data_copy.columns:
                data_copy['timestamp'] = data_copy['timestamp'].astype(str)
            
            data_copy.to_json(filename, orient='records', indent=4)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error exporting data: {e}")
        return False
