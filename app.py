import streamlit as st
import pandas as pd
import os
from utils import initialize_session_state
from data_processing import save_fan_data

# Initialize the app
st.set_page_config(
    page_title="FURIA Sports Fan Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# App title and description
st.title("FURIA Sports Fan Analytics")
st.markdown(
    """
    Welcome to the FURIA Sports Fan Analytics Platform! This tool helps understand fan demographics, 
    social media interactions, and engagement patterns to build stronger connections with the FURIA community.
    """
)

# Sidebar with navigation
st.sidebar.title("Navigation")
st.sidebar.info(
    """
    - **Home**: Fan Data Collection
    - **Fan Demographics**: Visualize fan demographics
    - **Social Media Analysis**: Track fan social media interactions
    - **Engagement Patterns**: Analyze fan engagement patterns
    - **Data Export**: Export collected data
    """
)

# Display images
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://images.unsplash.com/photo-1581397867105-8c988bd747e6", caption="Esports fans at event")
with col2:
    st.image("https://images.unsplash.com/photo-1504273066284-53fb4c703113", caption="FURIA fan engagement")
with col3:
    st.image("https://images.unsplash.com/photo-1612801798930-288967b6d1ef", caption="Esports tournament")

# Main content - Fan data collection form
st.header("Fan Data Collection")

with st.form("fan_data_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
    
    with col2:
        country = st.text_input("Country")
        city = st.text_input("City")
        fan_since = st.slider("Fan since (years)", 0, 10, 1)
        favorite_game = st.selectbox(
            "Favorite Esport Game", 
            ["Counter-Strike", "League of Legends", "Valorant", "Apex Legends", "Other"]
        )
        
    st.subheader("Social Media Information")
    col1, col2 = st.columns(2)
    
    with col1:
        instagram = st.text_input("Instagram Username (optional)")
        twitter = st.text_input("Twitter Username (optional)")
    
    with col2:
        twitch = st.text_input("Twitch Username (optional)")
        discord = st.text_input("Discord Username (optional)")
    
    st.subheader("Fan Engagement")
    engagement_type = st.multiselect(
        "How do you engage with FURIA?",
        [
            "Watch matches online", 
            "Attend live events", 
            "Purchase merchandise", 
            "Follow on social media",
            "Participate in fan communities",
            "Other"
        ]
    )
    
    purchase_frequency = st.select_slider(
        "How often do you purchase FURIA merchandise?",
        options=["Never", "Rarely", "Occasionally", "Frequently", "Very frequently"]
    )
    
    submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        if name and email and country:
            # Collect form data
            fan_data = {
                "name": name,
                "email": email,
                "age": age,
                "gender": gender,
                "country": country,
                "city": city,
                "fan_since": fan_since,
                "favorite_game": favorite_game,
                "instagram": instagram,
                "twitter": twitter,
                "twitch": twitch,
                "discord": discord,
                "engagement_type": engagement_type,
                "purchase_frequency": purchase_frequency,
                "timestamp": pd.Timestamp.now()
            }
            
            # Save the data and update session state
            save_fan_data(fan_data)
            
            st.success("Thank you for submitting your information! Your data helps us understand the FURIA fan community better.")
            st.balloons()
        else:
            st.error("Please fill in all required fields (Name, Email, and Country).")

# Analytics preview
st.header("Fan Analytics Preview")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Fan Distribution")
    st.image("https://images.unsplash.com/photo-1599474924187-334a4ae5bd3c", caption="Fan data analytics")
    st.info("Navigate to Fan Demographics page to see detailed visualizations.")

with col2:
    st.subheader("Social Media Engagement")
    st.image("https://images.unsplash.com/photo-1676565415277-a11304526519", caption="Social media interactions")
    st.info("Check the Social Media Analysis page to explore fan interactions.")

# Footer
st.markdown("---")
st.markdown("© 2023 FURIA Sports Fan Analytics Platform | Helping build stronger connections with fans")
