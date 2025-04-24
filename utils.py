import streamlit as st
import pandas as pd
import json
import os

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'fan_data' not in st.session_state:
        # Try to load existing data, or create an empty DataFrame
        try:
            if os.path.exists('fan_data.json'):
                with open('fan_data.json', 'r') as f:
                    data = json.load(f)
                st.session_state.fan_data = pd.DataFrame(data)
            else:
                st.session_state.fan_data = pd.DataFrame()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.session_state.fan_data = pd.DataFrame()
    
    if 'social_media_data' not in st.session_state:
        # This would typically come from API calls to social platforms
        st.session_state.social_media_data = pd.DataFrame()
    
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'age_range': (10, 100),
            'gender': [],
            'country': [],
            'favorite_game': [],
            'fan_since': (0, 10)
        }

def apply_filters(df):
    """Apply the current filters to the dataframe."""
    filtered_df = df.copy()
    
    # Apply age filter
    filtered_df = filtered_df[
        (filtered_df['age'] >= st.session_state.filters['age_range'][0]) &
        (filtered_df['age'] <= st.session_state.filters['age_range'][1])
    ]
    
    # Apply gender filter if selected
    if st.session_state.filters['gender']:
        filtered_df = filtered_df[filtered_df['gender'].isin(st.session_state.filters['gender'])]
    
    # Apply country filter if selected
    if st.session_state.filters['country']:
        filtered_df = filtered_df[filtered_df['country'].isin(st.session_state.filters['country'])]
    
    # Apply favorite game filter if selected
    if st.session_state.filters['favorite_game']:
        filtered_df = filtered_df[filtered_df['favorite_game'].isin(st.session_state.filters['favorite_game'])]
    
    # Apply fan since filter
    filtered_df = filtered_df[
        (filtered_df['fan_since'] >= st.session_state.filters['fan_since'][0]) &
        (filtered_df['fan_since'] <= st.session_state.filters['fan_since'][1])
    ]
    
    return filtered_df

def filter_sidebar():
    """Create a sidebar with filter options."""
    st.sidebar.header("Filter Data")
    
    # Age range filter
    st.session_state.filters['age_range'] = st.sidebar.slider(
        "Age Range",
        min_value=10,
        max_value=100,
        value=st.session_state.filters['age_range']
    )
    
    # Only show these filters if data exists
    if not st.session_state.fan_data.empty:
        # Gender filter
        available_genders = st.session_state.fan_data['gender'].unique().tolist()
        st.session_state.filters['gender'] = st.sidebar.multiselect(
            "Gender",
            options=available_genders,
            default=st.session_state.filters['gender']
        )
        
        # Country filter
        available_countries = st.session_state.fan_data['country'].unique().tolist()
        st.session_state.filters['country'] = st.sidebar.multiselect(
            "Country",
            options=available_countries,
            default=st.session_state.filters['country']
        )
        
        # Favorite game filter
        available_games = st.session_state.fan_data['favorite_game'].unique().tolist()
        st.session_state.filters['favorite_game'] = st.sidebar.multiselect(
            "Favorite Game",
            options=available_games,
            default=st.session_state.filters['favorite_game']
        )
    
    # Fan since filter
    st.session_state.filters['fan_since'] = st.sidebar.slider(
        "Fan Since (years)",
        min_value=0,
        max_value=10,
        value=st.session_state.filters['fan_since']
    )
    
    # Reset filters button
    if st.sidebar.button("Reset Filters"):
        st.session_state.filters = {
            'age_range': (10, 100),
            'gender': [],
            'country': [],
            'favorite_game': [],
            'fan_since': (0, 10)
        }
        st.rerun()
