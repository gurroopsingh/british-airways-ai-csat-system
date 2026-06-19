import os
import joblib

def load_prediction_artifacts():
    model_path = 'models/csat_prediction/saved_models/best_csat_model.joblib'
    vectorizer_path = 'models/csat_prediction/saved_models/tfidf_vectorizer.joblib'
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        raise FileNotFoundError("Model or vectorizer not found. Please run train_model.py first.")
        
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

def predict_csat(text: str) -> float:
    try:
        model, vectorizer = load_prediction_artifacts()
        # Ensure input is a list
        text_vec = vectorizer.transform([text])
        prediction = model.predict(text_vec)
        # Ensure score is within 1 to 5
        score = max(1.0, min(5.0, prediction[0]))
        return round(float(score), 2)
    except Exception as e:
        print(f"Error in predicting CSAT: {e}")
        return 3.0 # Neutral default

if __name__ == "__main__":
    sample_review = "The flight was delayed and the staff was extremely rude."
    print(f"Review: {sample_review}")
    print(f"Predicted CSAT: {predict_csat(sample_review)}")
