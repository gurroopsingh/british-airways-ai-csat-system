import os
import glob
import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure nltk packages are available
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

def find_csv():
    # Detect CSV in root folder
    csv_files = glob.glob('*.csv')
    if not csv_files:
        raise FileNotFoundError("No CSV file found in the project root directory.")
    # Assuming the first CSV is our target dataset
    return csv_files[0]

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # Lowercase conversion
    text = text.lower()
    # Punctuation removal
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenization
    tokens = word_tokenize(text)
    # Stopword removal
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    
    return " ".join(tokens)

def preprocess_data():
    csv_file = find_csv()
    print(f"Detected dataset: {csv_file}")
    
    df = pd.read_csv(csv_file)
    print("Detected columns:", df.columns.tolist())
    
    # Automatically determine the text column
    # Typically it's 'reviews', 'text', 'review_text', or 'content'
    text_col = None
    possible_cols = ['reviews', 'review_text', 'text', 'content', 'review']
    for col in df.columns:
        if col.lower() in possible_cols:
            text_col = col
            break
            
    # Fallback to the first object/string column if not found
    if not text_col:
        for col in df.columns:
            if df[col].dtype == 'object':
                text_col = col
                break
                
    if not text_col:
        raise ValueError("Could not automatically determine the text column from the dataset.")
        
    print(f"Selected text column for preprocessing: {text_col}")
    
    print("Preprocessing text data...")
    df['cleaned_text'] = df[text_col].apply(clean_text)
    
    # Save to data/processed
    os.makedirs('data/processed', exist_ok=True)
    out_path = 'data/processed/cleaned_reviews.csv'
    df.to_csv(out_path, index=False)
    print(f"Preprocessed data saved to {out_path}")

if __name__ == "__main__":
    preprocess_data()
