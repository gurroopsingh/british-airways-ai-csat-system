# AI-Driven Predictive Customer Satisfaction and Personalized Experience Recommendations for British Airways

## Problem Statement
British Airways processes thousands of customer reviews and feedback forms daily. Manually analyzing these reviews to assess customer satisfaction, identify recurring issues, and provide timely recommendations is slow and inefficient. Without an automated, intelligent system, addressing specific customer pain points (like flight delays, baggage handling, or customer service issues) takes too long, leading to a negative customer experience.

## Solution Overview
This project provides an AI-powered, end-to-end serverless architecture designed for British Airways to automatically analyze customer reviews. The system pre-processes the data, extracts sentiment using VADER, predicts a Customer Satisfaction (CSAT) score, models recurring topics, and explores Generative AI for personalized recommendations via Amazon Bedrock. A comprehensive Streamlit dashboard allows British Airways staff to view live analytics and run manual predictions. The solution is designed around AWS cloud services and is fully deployable.

## Dataset
The dataset consists of British Airways customer reviews stored in a CSV file (`british_airways_reviews.csv`). The pipeline automatically detects the dataset in the root directory, identifies the relevant text columns, and applies rigorous NLP preprocessing techniques including lowercase conversion, punctuation removal, tokenization, stopword removal, and lemmatization.

## Features
1. **Automated NLP Preprocessing**: Dynamically cleans raw review text data.
2. **Sentiment Analysis**: Uses VADER thresholding on compound scores for polarity detection (Positive, Neutral, Negative).
3. **CSAT Prediction**: Utilizes a trained Random Forest / XGBoost regressor model with TF-IDF features to predict a CSAT rating (1 to 5).
4. **Topic Modeling**: Evaluates BERTopic with guided seeds to extract key themes such as Flight Delays, Baggage Handling, Food Quality, Seat Comfort, and Customer Service.
5. **Recommendation Engine**: Designed to integrate with Amazon Bedrock (Anthropic Claude) for generating personalized recommendations based on the detected topic and sentiment.
6. **Streamlit Dashboard**: A professional dark-themed UI built with Plotly to visualize sentiment distribution, CSAT scores, and common issues.
7. **REST APIs**: FastAPI backend exposing endpoints for sentiment, prediction, and recommendations.
8. **Serverless Deployment**: Contains AWS Lambda function implementations for each API endpoint.

## Architecture
```text
British Airways Reviews Dataset
        ↓
Data Preprocessing (NLP Pipeline)
        ↓
Sentiment Analysis (VADER via Lambda)
        ↓
Customer Satisfaction Prediction (SageMaker Notebook → Lambda)
        ↓
Topic Modeling (BERTopic)
        ↓
Recommendation Engine (Bedrock — Explored)
        ↓
AWS Lambda + API Gateway
        ↓
Streamlit Dashboard
```

## AWS Services Used
| Service | Purpose |
|---------|---------|
| **Amazon S3** | Data lake for raw/processed datasets and serialized model artifacts (`.joblib`) |
| **AWS Lambda** | Serverless compute for sentiment, predict, and recommend endpoints |
| **Amazon API Gateway** | Exposes Lambda functions as RESTful APIs |
| **Amazon SageMaker** | Notebook environment for model training and evaluation |
| **Amazon Bedrock** | Configured to explore Generative AI for recommendation generation |
| **Amazon CloudWatch** | Monitoring and logging for Lambda function execution |
| **Streamlit** | Interactive frontend dashboard for live analytics |

> **Note:** The codebase contains local fallback logic to allow the project to be fully runnable locally without active AWS credentials.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gurroopsingh/british-airways-ai-csat-system.git
   cd british-airways-ai-csat-system
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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
├── architecture/
│   └── architecture.png
├── screenshots/
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
├── Week3_Report_Final.pdf
├── Week4_Report_Final.pdf
├── Week5_Report_Final.pdf
├── British_Airways_Premium_Presentation.pptx
├── requirements.txt
├── main.py
└── README.md
```

## Model Performance
- **Sentiment Analysis**: Uses VADER thresholding on compound scores for robust, zero-shot polarity detection.
- **CSAT Prediction**: Evaluates both Random Forest and XGBoost (if installed) using TF-IDF features. Performance metrics (MAE, RMSE, R²) are calculated and logged during the training phase.
- **Topic Modeling**: Employs BERTopic with guided seeds for domain-specific clustering (flight, baggage, food, seat, service).

## Deliverables
- `Week3_Report_Final.pdf` — Infrastructure Setup Report
- `Week4_Report_Final.pdf` — Backend and Serverless Development Report
- `Week5_Report_Final.pdf` — AI Service Integration and Generative AI Report
- `British_Airways_Premium_Presentation.pptx` — Conference-style Presentation

## Future Enhancements
- **Full AWS Deployment**: Provision AWS infrastructure using Terraform or AWS CDK.
- **Amazon Bedrock LLM Integration**: Fully integrate the recommendation engine with Anthropic Claude via Bedrock.
- **Advanced MLOps**: Migrate local model training to AWS SageMaker Pipelines with continuous model monitoring.
- **Real-Time Streaming**: Stream live reviews through Amazon Kinesis directly to the Lambda backend.

## References
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Repository](https://github.com/gurroopsingh/british-airways-ai-csat-system)
