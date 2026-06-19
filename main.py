import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import boto3
from datetime import datetime

# Import models
from models.sentiment.sentiment_model import SentimentIntensityAnalyzer
from models.csat_prediction.predict import predict_csat
from models.topic_modeling.bertopic_model import predict_topic
from models.recommendation_engine.recommendation_engine import generate_recommendation

app = FastAPI(title="British Airways AI CSAT System API")

class ReviewRequest(BaseModel):
    text: str

class RecommendRequest(BaseModel):
    topic_label: str
    sentiment: str

class FullReviewPipelineRequest(BaseModel):
    text: str

# DynamoDB Placeholder Setup
# dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
# table = dynamodb.Table('customer_reviews')

@app.post("/sentiment")
def analyze_sentiment_endpoint(request: ReviewRequest):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(request.text)
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = 'Positive'
    elif compound <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
        
    return {"sentiment": sentiment, "score": compound}

@app.post("/predict")
def predict_csat_endpoint(request: ReviewRequest):
    try:
        csat_score = predict_csat(request.text)
        return {"csat_score": csat_score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend")
def recommend_endpoint(request: RecommendRequest):
    recommendation = generate_recommendation(request.topic_label, request.sentiment)
    return {"recommendation": recommendation}

@app.post("/process_review")
def process_full_review(request: FullReviewPipelineRequest):
    text = request.text
    
    # 1. Sentiment
    analyzer = SentimentIntensityAnalyzer()
    compound = analyzer.polarity_scores(text)['compound']
    if compound >= 0.05: sentiment = 'Positive'
    elif compound <= -0.05: sentiment = 'Negative'
    else: sentiment = 'Neutral'
        
    # 2. Prediction
    csat_score = predict_csat(text)
    
    # 3. Topic Modeling
    topic = predict_topic(text)
    
    # 4. Recommendation
    recommendation = generate_recommendation(topic, sentiment)
    
    result = {
        "review_id": str(uuid.uuid4()),
        "review_text": text,
        "sentiment": sentiment,
        "predicted_score": csat_score,
        "topics": topic,
        "recommendation": recommendation,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # DynamoDB Integration Placeholder
    # try:
    #     table.put_item(Item=result)
    # except Exception as e:
    #     print(f"Failed to save to DynamoDB: {e}")
        
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
