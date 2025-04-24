import streamlit as st
import pandas as pd
import plotly.express as px
from utils import initialize_session_state, filter_sidebar, apply_filters
from data_processing import process_engagement_data
from visualization import plot_engagement_distribution, plot_purchase_frequency, plot_engagement_over_time

# Set page config
st.set_page_config(
    page_title="FURIA Fan Engagement Patterns",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Page title
st.title("FURIA Fan Engagement Patterns")
st.markdown("""
    Analyze how fans engage with FURIA across different channels and activities. 
    This page provides insights into engagement types, purchase behavior, and trends over time.
""")

# Sidebar for filters
filter_sidebar()

# Get filtered data
if 'fan_data' in st.session_state and not st.session_state.fan_data.empty:
    filtered_data = apply_filters(st.session_state.fan_data)
    
    # Display number of fans after filtering
    st.info(f"Analyzing engagement patterns for {len(filtered_data)} fans")
    
    # Process engagement data
    engagement_data = process_engagement_data(filtered_data)
    
    # Display engagement distribution
    st.subheader("Fan Engagement Types")
    engagement_fig = plot_engagement_distribution(engagement_data)
    if engagement_fig:
        st.plotly_chart(engagement_fig, use_container_width=True)
    
    # Display columns with engagement patterns
    col1, col2 = st.columns(2)
    
    with col1:
        # Purchase frequency
        purchase_fig = plot_purchase_frequency(filtered_data)
        if purchase_fig:
            st.plotly_chart(purchase_fig, use_container_width=True)
    
    with col2:
        # Engagement over time
        time_fig = plot_engagement_over_time(filtered_data)
        if time_fig:
            st.plotly_chart(time_fig, use_container_width=True)
    
    # Fan Loyalty Analysis
    st.subheader("Fan Loyalty Analysis")
    
    # Calculate engagement score based on different factors
    if not filtered_data.empty and 'fan_since' in filtered_data.columns:
        filtered_data['engagement_score'] = 0
        
        # Score based on fan_since (longer = higher score)
        filtered_data['engagement_score'] += filtered_data['fan_since'] * 10
        
        # Score based on purchase frequency
        purchase_scores = {
            "Never": 0,
            "Rarely": 5,
            "Occasionally": 15,
            "Frequently": 25,
            "Very frequently": 40
        }
        
        filtered_data['purchase_score'] = filtered_data['purchase_frequency'].map(purchase_scores)
        filtered_data['engagement_score'] += filtered_data['purchase_score']
        
        # Score based on engagement types (more types = higher score)
        if 'engagement_type' in filtered_data.columns:
            filtered_data['engagement_count'] = filtered_data['engagement_type'].apply(
                lambda x: len(x) if isinstance(x, list) else 0
            )
            filtered_data['engagement_score'] += filtered_data['engagement_count'] * 5
        
        # Score based on social media presence
        for platform in ['instagram', 'twitter', 'twitch', 'discord']:
            filtered_data['engagement_score'] += filtered_data[platform].notna().astype(int) * 5
        
        # Create fan segments
        def segment_fan(score):
            if score < 30:
                return "Casual"
            elif score < 60:
                return "Regular"
            elif score < 90:
                return "Dedicated"
            else:
                return "Superfan"
        
        filtered_data['fan_segment'] = filtered_data['engagement_score'].apply(segment_fan)
        
        # Display fan segments
        segments = filtered_data['fan_segment'].value_counts().reset_index()
        segments.columns = ['segment', 'count']
        
        segment_colors = {
            "Casual": "#90CAF9",  # Light blue
            "Regular": "#42A5F5",  # Medium blue
            "Dedicated": "#1976D2",  # Dark blue
            "Superfan": "#0D47A1"  # Very dark blue
        }
        
        segment_fig = px.pie(
            segments, 
            values='count', 
            names='segment',
            title='Fan Loyalty Segments',
            color='segment',
            color_discrete_map=segment_colors
        )
        
        segment_fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(segment_fig, use_container_width=True)
        
        # Display top fans
        st.subheader("Top FURIA Superfans")
        top_fans = filtered_data.sort_values('engagement_score', ascending=False).head(10)
        if not top_fans.empty:
            top_fans_display = top_fans[['name', 'country', 'fan_since', 'favorite_game', 'fan_segment', 'engagement_score']]
            st.dataframe(top_fans_display)
    
    # Engagement insights
    st.subheader("Engagement Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1504016798967-59a258e9386d", caption="Esports fan engagement")
    
    with col2:
        st.markdown("""
            ### Enhancing Fan Engagement
            
            Based on the analyzed patterns:
            
            - Most fans engage through **watching matches online** and **following on social media**
            - There's an opportunity to increase **merchandise purchases** among casual fans
            - Fan engagement tends to increase around tournament periods
            - Superfans represent the most valuable segment for brand advocacy
            
            Consider targeted engagement strategies for each fan segment to maximize loyalty and conversion.
        """)
else:
    st.image("https://images.unsplash.com/photo-1504273066284-53fb4c703113", caption="FURIA fan engagement")
    st.warning("No fan data available yet. Please collect fan information on the home page.")

# Footer
st.markdown("---")
st.markdown("© 2023 FURIA Sports Fan Analytics Platform | Engagement Patterns Module")
