#!/usr/bin/env python3

import sys
import json
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources if not downloaded
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# Load the list of stopwords
stop_words = set(stopwords.words('english'))

# Initialize the WordNet lemmatizer
lemmatizer = WordNetLemmatizer()

# Regular expression pattern to match words
word_pattern = re.compile(r'\b\w+\b')

# Set of punctuation characters
punctuation = set(string.punctuation)

for line in sys.stdin:
    try:
        record = json.loads(line)
        date = record['date']
        text = record['text']
        
        # Tokenize the text into words
        tokens = word_tokenize(text)
        
        processed_text = []
        
        for word in tokens:
            # Convert the word to lowercase
            word = word.lower()
            
            # Remove punctuation
            word = ''.join(char for char in word if char not in punctuation)
            
            # Check if it's a stop word or non-alphabetic word
            if word in stop_words or not word_pattern.match(word):
                continue
            
            # Lemmatize the word
            word = lemmatizer.lemmatize(word)
            
            processed_text.append(word)
        
        # Emit the date and processed text as key-value pairs
        output = {"date": date, "texts": " ".join(processed_text)}
        print(json.dumps(output))
    
    except ValueError as e:
        # Handle any JSON decoding errors
        continue

