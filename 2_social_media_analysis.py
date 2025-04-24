import streamlit as st
import pandas as pd
from utils import initialize_session_state, filter_sidebar, apply_filters
from visualization import plot_social_media_presence
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="FURIA Social Media Analysis",
    page_icon="📱",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Page title
st.title("FURIA Social Media Analysis")
st.markdown("""
    Analyze FURIA fan engagement across social media platforms. This page provides insights 
    into fan presence on various platforms, engagement patterns, and social media behavior.
""")

# Sidebar for filters
filter_sidebar()

# Get filtered data
if 'fan_data' in st.session_state and not st.session_state.fan_data.empty:
    filtered_data = apply_filters(st.session_state.fan_data)
    
    # Display number of fans after filtering
    st.info(f"Analyzing social media data for {len(filtered_data)} fans")
    
    # Display social media presence
    social_presence_fig = plot_social_media_presence(filtered_data)
    if social_presence_fig:
        st.plotly_chart(social_presence_fig, use_container_width=True)
    
    # Display social media engagement metrics
    st.subheader("Social Media Engagement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1676565415280-d1533965b4e5", caption="Social media analytics")
        
    with col2:
        st.markdown("""
            ### Social Media Integration
            
            In a production environment, this section would:
            
            - Pull real-time data from social media APIs
            - Track mentions, hashtags, and engagement with FURIA content
            - Monitor sentiment analysis of fan interactions
            - Identify influential fans and brand advocates
            
            The current version shows the social platforms where fans are present.
        """)
    
    # Social media platform breakdown
    st.subheader("Platform-Specific Analysis")
    
    # Create tabs for different platforms
    tabs = st.tabs(["Instagram", "Twitter", "Twitch", "Discord"])
    
    with tabs[0]:  # Instagram
        st.markdown("### Instagram Fan Analysis")
        
        # Count fans with Instagram
        instagram_fans = filtered_data[filtered_data['instagram'].notna()]
        st.metric("Fans with Instagram", len(instagram_fans))
        
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://images.unsplash.com/photo-1676565415274-15550cb4b75e", caption="Instagram analytics")
        with col2:
            st.markdown("""
                Instagram is a visual platform ideal for:
                - Sharing behind-the-scenes content
                - Highlighting team moments and victories
                - Showcasing merchandise and fan events
                - Running visual contests and promotions
                
                Consider cross-platform campaigns that start on Instagram and extend to other channels.
            """)
    
    with tabs[1]:  # Twitter
        st.markdown("### Twitter Fan Analysis")
        
        # Count fans with Twitter
        twitter_fans = filtered_data[filtered_data['twitter'].notna()]
        st.metric("Fans with Twitter", len(twitter_fans))
        
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://images.unsplash.com/photo-1607627000458-210e8d2bdb1d", caption="Twitter analytics")
        with col2:
            st.markdown("""
                Twitter is crucial for:
                - Real-time updates during matches
                - Quick announcements and news
                - Direct fan engagement and Q&As
                - Building community through hashtags
                
                Consider Twitter Spaces for live discussions with team members and fans.
            """)
    
    with tabs[2]:  # Twitch
        st.markdown("### Twitch Fan Analysis")
        
        # Count fans with Twitch
        twitch_fans = filtered_data[filtered_data['twitch'].notna()]
        st.metric("Fans with Twitch", len(twitch_fans))
        
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://images.unsplash.com/photo-1506499254543-b362909bf3b8", caption="Streaming analytics")
        with col2:
            st.markdown("""
                Twitch provides opportunities for:
                - Player streaming sessions
                - Behind-the-scenes team content
                - Fan tournaments and showcases
                - Direct interaction with the community
                
                Twitch subscriptions and donations can be a valuable revenue stream.
            """)
    
    with tabs[3]:  # Discord
        st.markdown("### Discord Fan Analysis")
        
        # Count fans with Discord
        discord_fans = filtered_data[filtered_data['discord'].notna()]
        st.metric("Fans with Discord", len(discord_fans))
        
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://images.unsplash.com/photo-1556155092-490a1ba16284", caption="Community analytics")
        with col2:
            st.markdown("""
                Discord is perfect for:
                - Building a dedicated community space
                - Organizing events and watch parties
                - Creating members-only content and perks
                - Facilitating fan-to-fan connections
                
                Consider creating specialized channels for different games and interests.
            """)
    
    # Cross-platform insights
    st.subheader("Cross-Platform Insights")
    
    # Calculate multi-platform users
    platforms = ['instagram', 'twitter', 'twitch', 'discord']
    filtered_data['platform_count'] = filtered_data[platforms].notna().sum(axis=1)
    
    platform_count = filtered_data['platform_count'].value_counts().sort_index().reset_index()
    platform_count.columns = ['number_of_platforms', 'count']
    
    # Create bar chart
    fig = px.bar(
        platform_count,
        x='number_of_platforms',
        y='count',
        title='Number of Social Platforms Used by Fans',
        labels={'number_of_platforms': 'Number of Platforms', 'count': 'Number of Fans'},
        color='number_of_platforms',
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show fans present on all platforms
    if st.checkbox("Show fans present on all platforms"):
        all_platform_fans = filtered_data[filtered_data['platform_count'] == len(platforms)]
        if not all_platform_fans.empty:
            st.dataframe(all_platform_fans[['name', 'email', 'country'] + platforms])
        else:
            st.info("No fans are present on all platforms.")
else:
    st.image("https://images.unsplash.com/photo-1676565415288-e5d295fff87a", caption="Social media data")
    st.warning("No fan data available yet. Please collect fan information on the home page.")

# Footer
st.markdown("---")
st.markdown("© 2023 FURIA Sports Fan Analytics Platform | Social Media Analysis Module")
