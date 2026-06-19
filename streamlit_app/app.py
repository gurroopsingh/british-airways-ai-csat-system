import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.sentiment.sentiment_model import SentimentIntensityAnalyzer
from models.csat_prediction.predict import predict_csat
from models.topic_modeling.bertopic_model import predict_topic
from models.recommendation_engine.recommendation_engine import generate_recommendation

st.set_page_config(page_title="British Airways AI CSAT", layout="wide", initial_sidebar_state="expanded")

# Load data safely
@st.cache_data
def load_data():
    path = 'data/processed/topics_reviews.csv'
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

df = load_data()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Sentiment Analysis", "CSAT Prediction", "Topic Modeling", "Recommendations", "Live Prediction Panel"])

st.title("British Airways AI-Driven Customer Experience Dashboard")

if page == "Dashboard":
    st.header("Overview")
    if df is not None:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Reviews Analyzed", len(df))
        col2.metric("Average CSAT Score", round(df['csat_score'].mean(), 2) if 'csat_score' in df else "N/A")
        
        dominant_topic = df['topic_label'].mode()[0] if 'topic_label' in df else "N/A"
        col3.metric("Most Frequent Issue", dominant_topic)
        
        st.markdown("### Key Metrics Breakdown")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Sentiment Distribution")
            if 'sentiment' in df.columns:
                fig = px.pie(df, names='sentiment', hole=0.3, color='sentiment',
                             color_discrete_map={'Positive':'#00cc96', 'Neutral':'#636efa', 'Negative':'#ef553b'})
                st.plotly_chart(fig, use_container_width=True)
                
        with col_chart2:
            st.subheader("Topic Frequencies")
            if 'topic_label' in df.columns:
                topic_counts = df['topic_label'].value_counts().reset_index()
                topic_counts.columns = ['Topic', 'Count']
                fig2 = px.bar(topic_counts, x='Topic', y='Count', color='Topic', template='plotly_dark')
                st.plotly_chart(fig2, use_container_width=True)
                
        st.subheader("CSAT Score Histogram")
        if 'csat_score' in df.columns:
            fig3 = px.histogram(df, x='csat_score', nbins=5, template='plotly_dark', color_discrete_sequence=['#ab63fa'])
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Data not found. Please run the preprocessing and modeling pipelines first.")

elif page == "Sentiment Analysis":
    st.header("Sentiment Analysis")
    if df is not None and 'sentiment' in df.columns:
        fig = px.pie(df, names='sentiment', title='Overall Sentiment Distribution')
        st.plotly_chart(fig)
        st.dataframe(df[['cleaned_text', 'sentiment', 'sentiment_score']].head(100))
    else:
        st.warning("Sentiment data not available.")

elif page == "CSAT Prediction":
    st.header("Customer Satisfaction Prediction")
    if df is not None and 'csat_score' in df.columns:
        fig = px.histogram(df, x='csat_score', title='Predicted CSAT Scores Distribution', nbins=5)
        st.plotly_chart(fig)
        st.dataframe(df[['cleaned_text', 'csat_score']].head(100))
    else:
        st.warning("CSAT data not available.")

elif page == "Topic Modeling":
    st.header("Topic Modeling Results")
    if df is not None and 'topic_label' in df.columns:
        topic_counts = df['topic_label'].value_counts().reset_index()
        topic_counts.columns = ['Topic', 'Count']
        fig = px.bar(topic_counts, x='Topic', y='Count', title='Prevalence of Topics')
        st.plotly_chart(fig)
        st.dataframe(df[['cleaned_text', 'topic_label']].head(100))
    else:
        st.warning("Topic data not available.")

elif page == "Recommendations":
    st.header("System Recommendations")
    st.markdown("Automated responses and recommendations based on aggregated topics.")
    if df is not None and 'topic_label' in df.columns:
        topics = df['topic_label'].unique()
        for t in topics:
            if t != "Other" and t != "General / Uncategorized":
                st.subheader(t)
                st.info(generate_recommendation(t, "Negative"))

elif page == "Live Prediction Panel":
    st.header("Live Customer Review Analysis")
    
    review_input = st.text_area("Enter Customer Review text:", "My flight was delayed by 3 hours and the staff was extremely unhelpful.")
    
    if st.button("Analyze Review"):
        with st.spinner("Analyzing..."):
            # Sentiment
            analyzer = SentimentIntensityAnalyzer()
            score = analyzer.polarity_scores(review_input)['compound']
            if score >= 0.05: sentiment = 'Positive'
            elif score <= -0.05: sentiment = 'Negative'
            else: sentiment = 'Neutral'
            
            # Predict
            try:
                csat = predict_csat(review_input)
            except Exception:
                csat = 3.0 # Default fallback
                
            # Topic
            try:
                topic = predict_topic(review_input)
            except Exception:
                topic = "General / Uncategorized"
                
            # Recommendation
            recommendation = generate_recommendation(topic, sentiment)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Sentiment", sentiment, f"{score:.2f}")
            col2.metric("Predicted CSAT", f"{csat:.1f} / 5.0")
            col3.metric("Detected Topic", topic)
            
            st.subheader("Suggested Action")
            st.success(recommendation)
