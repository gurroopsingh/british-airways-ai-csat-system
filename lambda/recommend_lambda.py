import json

def lambda_handler(event, context):
    """
    AWS Lambda handler for Recommendation Engine.
    Expects event['body'] to contain JSON with 'topic_label' and 'sentiment'.
    """
    try:
        body = json.loads(event.get('body', '{}'))
        topic_label = body.get('topic_label', 'Other')
        sentiment = body.get('sentiment', 'Neutral')
        
        if sentiment == 'Positive':
            recommendation = "Thank the customer for their positive feedback. Offer them a loyalty program upgrade."
        else:
            recommendations = {
                "Flight Delays": "Offer compensation points or complimentary lounge access for future flights.",
                "Baggage Handling": "Provide immediate baggage tracking support and a travel voucher for the inconvenience.",
                "Food Quality": "Offer a complimentary meal voucher or a free onboard meal for the next flight.",
                "Seat Comfort": "Offer a discounted upgrade to premium economy or extra legroom seats on the next flight.",
                "Customer Service": "Assign priority support for future queries and provide a formal apology from the customer relations team.",
                "General / Uncategorized": "Acknowledge the feedback and provide a general discount voucher for future travel.",
                "Other": "Acknowledge the feedback and provide a general discount voucher for future travel."
            }
            recommendation = recommendations.get(topic_label, "Investigate the issue and contact the customer for further assistance.")
            
        return {
            'statusCode': 200,
            'body': json.dumps({
                'recommendation': recommendation
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
