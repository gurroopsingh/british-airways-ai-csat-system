# AI-Driven Predictive Customer Satisfaction and Personalized Experience Recommendations for British Airways

## Problem Statement
British Airways processes thousands of customer reviews and feedback forms daily. Manually analyzing these reviews to assess customer satisfaction, identify recurring issues, and provide timely recommendations is slow and inefficient. Without an automated, intelligent system, addressing specific customer pain points (like flight delays, baggage handling, or customer service issues) takes too long, leading to a negative customer experience.

## Solution Overview
This project provides an AI-powered, end-to-end serverless architecture designed for British Airways to automatically analyze customer reviews. The system pre-processes the data, extracts sentiment, predicts a Customer Satisfaction (CSAT) score, models recurring topics using BERTopic, and generates personalized recommendations. A comprehensive Streamlit dashboard allows British Airways staff to view live analytics and run manual predictions. The solution is designed around AWS cloud services and is fully deployable.

## Dataset
The dataset consists of British Airways customer reviews stored in a CSV file (`british_airways_reviews.csv`). The pipeline automatically detects the dataset in the root directory, identifies the relevant text columns, and applies rigorous NLP preprocessing techniques including lowercase conversion, punctuation removal, tokenization, stopword removal, and lemmatization.

## Features
1. **Automated NLP Preprocessing**: Dynamically cleans raw review text data.
2. **Sentiment Analysis**: Uses VADER (and optionally DistilBERT) to categorize reviews into Positive, Neutral, or Negative.
3. **CSAT Prediction**: Utilizes a trained Random Forest / XGBoost regressor model with TF-IDF features to predict a synthetic CSAT rating (1 to 5).
4. **Topic Modeling**: Leverages BERTopic to extract key themes such as Flight Delays, Baggage Handling, Food Quality, Seat Comfort, and Customer Service.
5. **Recommendation Engine**: Generates rule-based or generative AI (Amazon Bedrock) personalized recommendations based on the detected topic and sentiment.
6. **Streamlit Dashboard**: A professional dark-themed UI built with Plotly to visualize sentiment distribution, CSAT scores, and common issues.
7. **REST APIs**: FastAPI backend exposing endpoints for sentiment, prediction, and recommendations.
8. **Serverless Deployment Ready**: Contains AWS Lambda and DynamoDB handler implementations.

## Architecture
```text
British Airways Reviews Dataset
↓
Data Preprocessing
↓
Sentiment Analysis (Comprehend/BERT)
↓
Customer Satisfaction Prediction (SageMaker)
↓
Topic Modeling (BERTopic/LDA)
↓
Recommendation Engine (Bedrock)
↓
AWS Lambda + API Gateway
↓
DynamoDB
↓
Streamlit Dashboard
```

## AWS Services Used
- **Amazon S3**: For storing raw/processed datasets and model artifacts.
- **Amazon SageMaker**: For training and hosting the CSAT prediction model.
- **AWS Lambda**: Serverless compute for sentiment, predict, and recommend endpoints.
- **API Gateway**: To expose Lambda functions as RESTful APIs.
- **Amazon DynamoDB**: NoSQL database for storing processed reviews and predictions.
- **Amazon Comprehend**: For managed sentiment analysis (alternative to VADER).
- **Amazon Bedrock**: For generating Generative AI based personalized recommendations.

*Note: The current codebase contains integration placeholders and local fallback logic to allow the project to be fully runnable locally without active AWS credentials.*

## Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repo-url>
   cd british-airways-ai-csat-system
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. **Run the Data Pipeline**:
   Ensure your CSV dataset is placed in the root folder, then run the pipeline scripts in order:
   ```bash
   python data/preprocess.py
   python models/sentiment/sentiment_model.py
   python models/csat_prediction/train_model.py
   python models/topic_modeling/bertopic_model.py
   ```

2. **Start the REST API (FastAPI)**:
   ```bash
   uvicorn main:app --reload
   ```
   API Docs available at: `http://localhost:8000/docs`

3. **Start the Streamlit Dashboard**:
   ```bash
   streamlit run streamlit_app/app.py
   ```

## Folder Structure
```
british-airways-ai-csat-system/
├── data/
│   ├── raw/
│   ├── processed/
│   └── preprocess.py
├── models/
│   ├── sentiment/
│   │   └── sentiment_model.py
│   ├── csat_prediction/
│   │   ├── train_model.py
│   │   └── predict.py
│   ├── topic_modeling/
│   │   └── bertopic_model.py
│   └── recommendation_engine/
│       └── recommendation_engine.py
├── lambda/
│   ├── sentiment_lambda.py
│   ├── predict_lambda.py
│   └── recommend_lambda.py
├── api/
├── streamlit_app/
│   └── app.py
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_sentiment_analysis.ipynb
│   ├── 03_csat_prediction.ipynb
│   ├── 04_topic_modeling.ipynb
│   └── 05_recommendation_engine.ipynb
├── architecture/
├── screenshots/
├── requirements.txt
├── README.md
└── main.py
```

## Model Performance
- **Sentiment Analysis**: Uses VADER thresholding on compound scores for robust, zero-shot polarity detection.
- **CSAT Prediction**: Automatically evaluates both Random Forest and XGBoost (if installed) using TF-IDF features. Performance metrics (MAE, RMSE, R²) are calculated and logged during the training phase.
- **Topic Modeling**: Employs BERTopic with guided seeds for domain-specific accuracy (flight, baggage, food, seat, service).

## Future Enhancements
- **Full AWS Deployment**: Provision AWS infrastructure using Terraform or AWS CDK.
- **Amazon Bedrock LLM Integration**: Fully integrate the placeholder recommendation engine with Anthropic Claude v2 via Bedrock to replace rule-based logic.
- **Advanced MLOps**: Migrate local model training to AWS SageMaker Pipelines with continuous model monitoring.
- **Real-Time Streaming**: Stream live tweets and reviews through Amazon Kinesis directly to the Lambda backend.
