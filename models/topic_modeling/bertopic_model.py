import pandas as pd
import os
import joblib
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

def run_topic_modeling():
    file_path = 'data/processed/sentiment_reviews.csv'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
        
    print("Loading data for topic modeling...")
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['cleaned_text'])
    
    docs = df['cleaned_text'].tolist()
    
    print("Initializing BERTopic...")
    # Using a simple vectorizer to ensure fast and stable runs
    vectorizer_model = CountVectorizer(stop_words="english")
    
    # Pre-defined seed topics (optional, helps BERTopic steer towards relevant categories)
    seed_topic_list = [
        ["flight", "delay", "late", "waiting", "time"],
        ["baggage", "luggage", "lost", "claim", "bag"],
        ["food", "meal", "drink", "tasteless", "cold"],
        ["seat", "comfort", "legroom", "space", "cramped"],
        ["service", "rude", "staff", "attendant", "unprofessional"]
    ]
    
    topic_model = BERTopic(vectorizer_model=vectorizer_model, seed_topic_list=seed_topic_list, verbose=True)
    
    print("Fitting BERTopic model...")
    topics, probs = topic_model.fit_transform(docs)
    
    df['topic_id'] = topics
    
    # Map topics to labels based on keywords
    topic_info = topic_model.get_topic_info()
    
    def map_topic_label(topic_id):
        if topic_id == -1:
            return "General / Uncategorized"
        
        words = [word for word, _ in topic_model.get_topic(topic_id)]
        words_str = " ".join(words)
        
        if any(w in words_str for w in ["delay", "time", "hour", "late", "wait"]): return "Flight Delays"
        if any(w in words_str for w in ["bag", "luggage", "lost", "claim"]): return "Baggage Handling"
        if any(w in words_str for w in ["food", "meal", "drink"]): return "Food Quality"
        if any(w in words_str for w in ["seat", "comfort", "legroom", "space"]): return "Seat Comfort"
        if any(w in words_str for w in ["staff", "rude", "service", "crew"]): return "Customer Service"
        
        return "Other"

    print("Assigning topic labels...")
    df['topic_label'] = df['topic_id'].apply(map_topic_label)
    
    # Save the model
    os.makedirs('models/topic_modeling/saved_models', exist_ok=True)
    model_path = 'models/topic_modeling/saved_models/bertopic_model'
    topic_model.save(model_path, serialization="safetensors", save_ctfidf=True)
    print(f"BERTopic model saved to {model_path}")
    
    out_path = 'data/processed/topics_reviews.csv'
    df.to_csv(out_path, index=False)
    print(f"Topics saved to {out_path}")

def predict_topic(text: str):
    try:
        model_path = 'models/topic_modeling/saved_models/bertopic_model'
        topic_model = BERTopic.load(model_path)
        topics, _ = topic_model.transform([text])
        topic_id = topics[0]
        
        if topic_id == -1:
            return "General / Uncategorized"
            
        words = [word for word, _ in topic_model.get_topic(topic_id)]
        words_str = " ".join(words)
        
        if any(w in words_str for w in ["delay", "time", "hour", "late", "wait"]): return "Flight Delays"
        if any(w in words_str for w in ["bag", "luggage", "lost", "claim"]): return "Baggage Handling"
        if any(w in words_str for w in ["food", "meal", "drink"]): return "Food Quality"
        if any(w in words_str for w in ["seat", "comfort", "legroom", "space"]): return "Seat Comfort"
        if any(w in words_str for w in ["staff", "rude", "service", "crew"]): return "Customer Service"
        
        return "Other"
    except Exception as e:
        print(f"Error in predicting topic: {e}")
        return "General / Uncategorized"

if __name__ == "__main__":
    run_topic_modeling()
