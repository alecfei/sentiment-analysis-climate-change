#!/usr/bin/env python3

import sys
import json
import re
from nltk.corpus import stopwords

# Regular expression pattern to match words
word_pattern = re.compile(r"\b\w+\b")

# Set of stop words
# Uncomment the next two lines when needed
#import nltk
#nltk.download('stopwords')
stop_words = set(stopwords.words("english"))

# Read JSON records from standard input
for line in sys.stdin:
    try:
        record = json.loads(line)
        if "text" in record:
            # Extract the "text" field from the JSON record
            text = record["text"]

            # Tokenize the text into words
            words = re.findall(word_pattern, text)

            # Emit each triple word with count 1, excluding stop words
            for i in range(len(words) - 2):
                triple_word = words[i].lower() + " " + words[i + 1].lower() + " " + words[i + 2].lower()
                if not any(word in stop_words for word in triple_word.split()):
                    print("%s\t%d" % (triple_word, 1))
    except ValueError:
        pass
