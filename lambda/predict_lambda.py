import json
import joblib
import os

# Note: In a real AWS Lambda environment, the model and vectorizer would be loaded from Amazon S3
# For local simulation, we load from the local file system
def load_prediction_artifacts():
    model_path = '/opt/ml/model/best_csat_model.joblib'
    vectorizer_path = '/opt/ml/model/tfidf_vectorizer.joblib'
    
    # Fallback to local path if not in Lambda
    if not os.path.exists(model_path):
        model_path = '../models/csat_prediction/saved_models/best_csat_model.joblib'
        vectorizer_path = '../models/csat_prediction/saved_models/tfidf_vectorizer.joblib'
        
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

def lambda_handler(event, context):
    """
    AWS Lambda handler for CSAT Prediction.
    Expects event['body'] to contain JSON with a 'text' key.
    """
    try:
        body = json.loads(event.get('body', '{}'))
        text = body.get('text', '')
        
        if not text:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing text parameter'})
            }
            
        model, vectorizer = load_prediction_artifacts()
        text_vec = vectorizer.transform([text])
        prediction = model.predict(text_vec)
        score = max(1.0, min(5.0, prediction[0]))
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'csat_score': round(score, 2)
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
