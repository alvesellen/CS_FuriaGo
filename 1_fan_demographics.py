import streamlit as st
import pandas as pd
import plotly.express as px
from utils import initialize_session_state, filter_sidebar, apply_filters
from visualization import (
    plot_age_distribution, 
    plot_gender_distribution, 
    plot_country_distribution, 
    plot_favorite_games,
    plot_fan_timeline
)

# Set page config
st.set_page_config(
    page_title="FURIA Fan Demographics",
    page_icon="👥",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Page title
st.title("FURIA Fan Demographics")
st.markdown("""
    Understand the FURIA fan base with detailed demographic visualizations. 
    This page provides insights into fan age distribution, gender breakdown, geographic location, 
    favorite games, and how long they've been supporting FURIA.
""")

# Sidebar for filters
filter_sidebar()

# Get filtered data
if 'fan_data' in st.session_state and not st.session_state.fan_data.empty:
    filtered_data = apply_filters(st.session_state.fan_data)
    
    # Display number of fans after filtering
    st.info(f"Showing data for {len(filtered_data)} fans")
    
    # Display fan demographics in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution
        age_fig = plot_age_distribution(filtered_data)
        if age_fig:
            st.plotly_chart(age_fig, use_container_width=True)
        
        # Country distribution
        country_fig = plot_country_distribution(filtered_data)
        if country_fig:
            st.plotly_chart(country_fig, use_container_width=True)
        
        # Fan timeline
        fan_timeline_fig = plot_fan_timeline(filtered_data)
        if fan_timeline_fig:
            st.plotly_chart(fan_timeline_fig, use_container_width=True)
    
    with col2:
        # Gender distribution
        gender_fig = plot_gender_distribution(filtered_data)
        if gender_fig:
            st.plotly_chart(gender_fig, use_container_width=True)
        
        # Favorite games
        games_fig = plot_favorite_games(filtered_data)
        if games_fig:
            st.plotly_chart(games_fig, use_container_width=True)
    
    # Fan overview
    st.subheader("Fan Data Overview")
    
    # Show the raw data in a table
    if st.checkbox("Show raw data"):
        st.dataframe(filtered_data)
else:
    st.image("https://images.unsplash.com/photo-1591754060004-f91c95f5cf05", caption="FURIA fans cheering")
    st.warning("No fan data available yet. Please collect fan information on the home page.")

# Display an insight about the data
st.header("Fan Demographics Insights")
col1, col2 = st.columns(2)

with col1:
    st.image("https://images.unsplash.com/photo-1456428746267-a1756408f782", caption="Sports analytics")
    
with col2:
    st.markdown("""
        ### Understanding Your Audience
        
        Demographic insights help FURIA:
        
        - Target marketing campaigns more effectively
        - Develop merchandise that appeals to the core fan base
        - Identify untapped fan segments for growth
        - Tailor content to different age groups and regions
        
        Use the filters on the left to explore different fan segments and discover patterns.
    """)

# Footer
st.markdown("---")
st.markdown("© 2023 FURIA Sports Fan Analytics Platform | Fan Demographics Module")
