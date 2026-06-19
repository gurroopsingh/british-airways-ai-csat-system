import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

def train_csat_model():
    file_path = 'data/processed/sentiment_reviews.csv'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found. Run sentiment_model.py first.")
        
    print("Loading sentiment data...")
    df = pd.read_csv(file_path)
    
    # Drop NaNs
    df = df.dropna(subset=['cleaned_text', 'csat_score'])
    
    X = df['cleaned_text']
    y = df['csat_score']
    
    print("Vectorizing text data using TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vec = vectorizer.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    
    rf_mae = mean_absolute_error(y_test, rf_preds)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
    rf_r2 = r2_score(y_test, rf_preds)
    
    print(f"Random Forest - MAE: {rf_mae:.4f}, RMSE: {rf_rmse:.4f}, R²: {rf_r2:.4f}")
    
    best_model = rf_model
    best_name = "RandomForest"
    best_preds = rf_preds
    
    if XGB_AVAILABLE:
        print("Training XGBoost Regressor...")
        xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
        xgb_model.fit(X_train, y_train)
        xgb_preds = xgb_model.predict(X_test)
        
        xgb_mae = mean_absolute_error(y_test, xgb_preds)
        xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_preds))
        xgb_r2 = r2_score(y_test, xgb_preds)
        
        print(f"XGBoost - MAE: {xgb_mae:.4f}, RMSE: {xgb_rmse:.4f}, R²: {xgb_r2:.4f}")
        
        if xgb_r2 > rf_r2:
            best_model = xgb_model
            best_name = "XGBoost"
            print("XGBoost selected as the best model.")
        else:
            print("Random Forest selected as the best model.")
            
    # Save the best model and vectorizer
    os.makedirs('models/csat_prediction/saved_models', exist_ok=True)
    model_path = 'models/csat_prediction/saved_models/best_csat_model.joblib'
    vectorizer_path = 'models/csat_prediction/saved_models/tfidf_vectorizer.joblib'
    
    joblib.dump(best_model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"Best model ({best_name}) saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")

if __name__ == "__main__":
    train_csat_model()
