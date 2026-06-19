import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment():
    file_path = 'data/processed/cleaned_reviews.csv'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found. Run preprocess.py first.")
        
    print("Loading preprocessed data...")
    df = pd.read_csv(file_path)
    
    if 'cleaned_text' not in df.columns:
        raise ValueError("Column 'cleaned_text' not found in dataset. Preprocessing step may have failed.")
        
    print("Initializing VADER Sentiment Analyzer...")
    analyzer = SentimentIntensityAnalyzer()
    
    def get_sentiment(text):
        if not isinstance(text, str):
            return 0.0, 'Neutral'
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            sentiment = 'Positive'
        elif compound <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
            
        return compound, sentiment

    print("Running sentiment analysis...")
    # Apply sentiment analysis
    sentiment_results = df['cleaned_text'].apply(get_sentiment)
    
    df['sentiment_score'] = [res[0] for res in sentiment_results]
    df['sentiment'] = [res[1] for res in sentiment_results]
    
    # Since the original dataset lacks a CSAT/rating column, we derive a synthetic CSAT rating (1 to 5)
    # based on the VADER compound score for the prediction model to train on.
    def map_to_csat(score):
        # Map compound score (-1.0 to 1.0) to CSAT score (1 to 5)
        # -1.0 to -0.6 -> 1
        # -0.6 to -0.2 -> 2
        # -0.2 to  0.2 -> 3
        #  0.2 to  0.6 -> 4
        #  0.6 to  1.0 -> 5
        if score <= -0.6: return 1
        elif score <= -0.2: return 2
        elif score <= 0.2: return 3
        elif score <= 0.6: return 4
        else: return 5
        
    df['csat_score'] = df['sentiment_score'].apply(map_to_csat)
    
    out_path = 'data/processed/sentiment_reviews.csv'
    df.to_csv(out_path, index=False)
    print(f"Sentiment analysis completed. Results saved to {out_path}")

if __name__ == "__main__":
    analyze_sentiment()
