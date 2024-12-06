import streamlit as st
import pandas as pd
import plotly.express as px

# Title for the app
st.title("Influencer Sentiment and Engagement Analysis")

# App description
st.markdown("""
This app allows you to analyze influencer data to determine the best candidates based on sentiment analysis and engagement metrics.
Upload the necessary files to begin.
""")

# Upload CSV files
st.sidebar.header("Upload Files")
influencers_file = st.sidebar.file_uploader("Upload Influencers Data CSV", type=["csv"])
sentiment_file = st.sidebar.file_uploader("Upload Sentiment Analysis CSV", type=["csv"])

# Initialize dataframes
influencers_data = None
sentiment_data = None

# Load and preview Influencer Data
if influencers_file:
    influencers_data = pd.read_csv(influencers_file)
    st.header("Influencers Data")
    st.write(influencers_data.head())
    if 'Channel Name' in influencers_data.columns and 'Engagement Rate' in influencers_data.columns:
        st.subheader("Engagement Metrics")
        fig = px.bar(
            influencers_data,
            x='Channel Name',
            y='Engagement Rate',
            title='Engagement Rate by Influencer',
            labels={'Engagement Rate': 'Engagement Rate (%)'},
            color='Engagement Rate'
        )
        st.plotly_chart(fig)

# Load and preview Sentiment Analysis Data
if sentiment_file:
    sentiment_data = pd.read_csv(sentiment_file)
    st.header("Sentiment Analysis Data")
    st.write(sentiment_data.head())
    if 'Channel Name' in sentiment_data.columns and 'Positive' in sentiment_data.columns:
        st.subheader("Sentiment Metrics")
        fig = px.bar(
            sentiment_data,
            x='Channel Name',
            y=['Positive', 'Neutral', 'Negative'],
            title='Sentiment Distribution by Influencer',
            labels={'value': 'Sentiment Score', 'variable': 'Sentiment'},
            barmode='group'
        )
        st.plotly_chart(fig)

# Combine and display results
if influencers_data is not None and sentiment_data is not None:
    st.header("Combined Analysis")
    combined_data = pd.merge(influencers_data, sentiment_data, on='Channel Name', how='inner')
    st.write(combined_data.head())
    
    # Example visualization for combined metrics
    st.subheader("Subscriber Count vs Engagement Rate")
    fig = px.scatter(
        combined_data,
        x='Subscriber Count',
        y='Engagement Rate',
        size='Positive',  # Bubble size based on positive sentiment
        color='Channel Name',
        title='Subscribers vs Engagement Rate with Sentiment Size'
    )
    st.plotly_chart(fig)
    
    st.subheader("Top Influencers by Total Score")
    top_influencers = combined_data.sort_values(by='Total Score', ascending=False).head(5)
    st.write(top_influencers[['Channel Name', 'Total Score']])

# Footer
st.markdown("---")
st.write("Created by [Your Name]. Powered by Streamlit.")
