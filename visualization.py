import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_age_distribution(data):
    """Plot the age distribution of fans."""
    if data.empty or 'age' not in data.columns:
        st.warning("No age data available for visualization.")
        return None
    
    fig = px.histogram(
        data, 
        x='age',
        nbins=20,
        title='Age Distribution of FURIA Fans',
        labels={'age': 'Age', 'count': 'Number of Fans'},
        color_discrete_sequence=['#1A237E']
    )
    
    fig.update_layout(
        xaxis_title='Age',
        yaxis_title='Number of Fans',
        bargap=0.1
    )
    
    return fig

def plot_gender_distribution(data):
    """Plot the gender distribution of fans."""
    if data.empty or 'gender' not in data.columns:
        st.warning("No gender data available for visualization.")
        return None
    
    gender_counts = data['gender'].value_counts().reset_index()
    gender_counts.columns = ['gender', 'count']
    
    fig = px.pie(
        gender_counts, 
        values='count', 
        names='gender',
        title='Gender Distribution of FURIA Fans',
        color_discrete_sequence=px.colors.sequential.Blues
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def plot_country_distribution(data):
    """Plot the geographic distribution of fans by country."""
    if data.empty or 'country' not in data.columns:
        st.warning("No country data available for visualization.")
        return None
    
    country_counts = data['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'count']
    
    fig = px.bar(
        country_counts.head(10), 
        x='country',
        y='count',
        title='Top 10 Countries of FURIA Fans',
        labels={'country': 'Country', 'count': 'Number of Fans'},
        color='count',
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Number of Fans'
    )
    
    return fig

def plot_favorite_games(data):
    """Plot the distribution of favorite games."""
    if data.empty or 'favorite_game' not in data.columns:
        st.warning("No favorite game data available for visualization.")
        return None
    
    game_counts = data['favorite_game'].value_counts().reset_index()
    game_counts.columns = ['favorite_game', 'count']
    
    fig = px.pie(
        game_counts, 
        values='count', 
        names='favorite_game',
        title='Favorite Games Among FURIA Fans',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def plot_fan_timeline(data):
    """Plot how long people have been fans."""
    if data.empty or 'fan_since' not in data.columns:
        st.warning("No fan duration data available for visualization.")
        return None
    
    fan_since_counts = data['fan_since'].value_counts().sort_index().reset_index()
    fan_since_counts.columns = ['fan_since', 'count']
    
    fig = px.line(
        fan_since_counts, 
        x='fan_since',
        y='count',
        title='How Long People Have Been FURIA Fans',
        labels={'fan_since': 'Years as Fan', 'count': 'Number of Fans'},
        markers=True
    )
    
    fig.update_layout(
        xaxis_title='Years as Fan',
        yaxis_title='Number of Fans',
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 1
        )
    )
    
    return fig

def plot_engagement_distribution(engagement_data):
    """Plot the distribution of fan engagement types."""
    if engagement_data.empty:
        st.warning("No engagement data available for visualization.")
        return None
    
    fig = px.bar(
        engagement_data, 
        x='engagement_type',
        y='count',
        title='Types of Fan Engagement with FURIA',
        labels={'engagement_type': 'Engagement Type', 'count': 'Number of Fans'},
        color='count',
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    fig.update_layout(
        xaxis_title='Engagement Type',
        yaxis_title='Number of Fans'
    )
    
    return fig

def plot_social_media_presence(data):
    """Plot the social media presence of fans."""
    if data.empty:
        st.warning("No social media data available for visualization.")
        return None
    
    # Count non-empty social media handles
    social_counts = {
        'Instagram': data['instagram'].notna().sum(),
        'Twitter': data['twitter'].notna().sum(),
        'Twitch': data['twitch'].notna().sum(),
        'Discord': data['discord'].notna().sum()
    }
    
    social_df = pd.DataFrame({
        'platform': list(social_counts.keys()),
        'count': list(social_counts.values())
    })
    
    fig = px.bar(
        social_df, 
        x='platform',
        y='count',
        title='FURIA Fans Social Media Presence',
        labels={'platform': 'Social Media Platform', 'count': 'Number of Fans'},
        color='platform',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_layout(
        xaxis_title='Social Media Platform',
        yaxis_title='Number of Fans'
    )
    
    return fig

def plot_purchase_frequency(data):
    """Plot the merchandise purchase frequency distribution."""
    if data.empty or 'purchase_frequency' not in data.columns:
        st.warning("No purchase frequency data available for visualization.")
        return None
    
    purchase_order = ["Never", "Rarely", "Occasionally", "Frequently", "Very frequently"]
    purchase_counts = data['purchase_frequency'].value_counts().reindex(purchase_order).reset_index()
    purchase_counts.columns = ['purchase_frequency', 'count']
    
    fig = px.bar(
        purchase_counts, 
        x='purchase_frequency',
        y='count',
        title='FURIA Merchandise Purchase Frequency',
        labels={'purchase_frequency': 'Purchase Frequency', 'count': 'Number of Fans'},
        color='purchase_frequency',
        color_discrete_sequence=px.colors.sequential.Blues
    )
    
    fig.update_layout(
        xaxis_title='Purchase Frequency',
        yaxis_title='Number of Fans',
        xaxis={'categoryorder':'array', 'categoryarray':purchase_order}
    )
    
    return fig

def plot_engagement_over_time(data):
    """Plot fan engagement trends over time."""
    if data.empty or 'timestamp' not in data.columns:
        st.warning("No timestamp data available for visualization.")
        return None
    
    # Group by date
    data['date'] = data['timestamp'].dt.date
    engagement_over_time = data.groupby('date').size().reset_index(name='count')
    
    fig = px.line(
        engagement_over_time, 
        x='date',
        y='count',
        title='Fan Engagement Over Time',
        labels={'date': 'Date', 'count': 'Number of Fan Submissions'},
        markers=True
    )
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Number of Fan Submissions'
    )
    
    return fig
