import json
import os

def create_notebook(filename, title, code):
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {title}\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [line + '\n' for line in code.split('\n')]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    os.makedirs('notebooks', exist_ok=True)
    with open(f'notebooks/{filename}', 'w') as f:
        json.dump(notebook, f, indent=1)

create_notebook(
    '01_data_preprocessing.ipynb', 
    'Module 1: Data Preprocessing',
    '''import os\nimport glob\nimport pandas as pd\n\n# Automatically locate the CSV file in the root folder\ncsv_files = glob.glob("../*.csv")\nif csv_files:\n    df = pd.read_csv(csv_files[0])\n    print(df.head())\nelse:\n    print("CSV not found")'''
)

create_notebook(
    '02_sentiment_analysis.ipynb', 
    'Module 2: Sentiment Analysis',
    '''import pandas as pd\nfrom vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer\n\n# Example Sentiment Analysis\nanalyzer = SentimentIntensityAnalyzer()\nscores = analyzer.polarity_scores("The flight was amazing and the crew was helpful.")\nprint(scores)'''
)

create_notebook(
    '03_csat_prediction.ipynb', 
    'Module 3: Customer Satisfaction Prediction',
    '''from sklearn.ensemble import RandomForestRegressor\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nimport numpy as np\n\n# Example prediction setup\ntexts = ["Bad delay", "Great service"]\nlabels = [1, 5]\n\nvec = TfidfVectorizer()\nX = vec.fit_transform(texts)\nmodel = RandomForestRegressor()\nmodel.fit(X, labels)\nprint("Model trained.")'''
)

create_notebook(
    '04_topic_modeling.ipynb', 
    'Module 4: Topic Modeling',
    '''from bertopic import BERTopic\n\n# Example BERTopic\ndocs = ["The flight was delayed", "The luggage was lost"]\ntopic_model = BERTopic()\n# topics, probs = topic_model.fit_transform(docs)\nprint("BERTopic initialized.")'''
)

create_notebook(
    '05_recommendation_engine.ipynb', 
    'Module 5: Recommendation Engine',
    '''def recommend(topic):\n    if topic == "Flight Delays":\n        return "Offer compensation"\n    return "Acknowledge issue"\n\nprint(recommend("Flight Delays"))'''
)
