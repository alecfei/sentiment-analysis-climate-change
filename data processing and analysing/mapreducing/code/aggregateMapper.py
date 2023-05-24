#!/usr/bin/env python3

import sys
import random
import json

def mapper():
    for line in sys.stdin:
        record = json.loads(line)
        date = record['date'][:10]  # Extract the year-month-day portion
        text = record['text']
        random_key = random.random()  # Generate a random key for secondary sorting
        emit(date, random_key, text)

def emit(date, random_key, text):
    output = {'date': date, 'text': text}
    print(f"{date}\t{random_key}\t{json.dumps(output)}")

if __name__ == "__main__":
    mapper()

