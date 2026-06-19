import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def lambda_handler(event, context):
    """
    AWS Lambda handler for Sentiment Analysis.
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
            
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            sentiment = 'Positive'
        elif compound <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
            
        return {
            'statusCode': 200,
            'body': json.dumps({
                'sentiment': sentiment,
                'score': compound
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
