#!/usr/bin/env python3

import sys
import json
from nltk.sentiment import SentimentIntensityAnalyzer

# Execute below when needed
#import nltk
#nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

for line in sys.stdin:
    try:
        record = json.loads(line)
        date = record['date']
        text = record['texts']
        
        # Perform sentiment analysis on the text
        sentiment = sia.polarity_scores(text)['compound']
        
        # Emit the date, text, and sentiment as key-value pairs
        output = {"date": date, "texts": text, "sentiment": sentiment}
        print(json.dumps(output))
    
    except ValueError as e:
        # Handle any JSON decoding errors
        continue
