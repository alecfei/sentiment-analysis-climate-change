#!/usr/bin/env python3

import sys
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

# Download NLTK resources
nltk.download('punkt')
#nltk.download('stopwords') /already downloaded
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load stopwords
stop_words = set(stopwords.words('english'))

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def process_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stopwords and punctuation
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words and token not in string.punctuation]

    # Lemmatize the tokens
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    return lemmatized_tokens

for line in sys.stdin:
    record = json.loads(line)
    if 'text' in record:
        date = record.get('date', '')  # Retrieve the "date" field
        text = record['text']
        # Process the text
        processed_text = process_text(text)
        # Update the record with the processed text
        record['date'] = date  # Keep the "date" field
        record['text'] = processed_text
    print(json.dumps(record))
