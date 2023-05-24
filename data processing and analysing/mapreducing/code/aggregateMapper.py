#!/usr/bin/env python3

import sys
import random
import json

def mapper():
    for line in sys.stdin:
        record = json.loads(line)
        date = record['date'][:10]  # Extract the year-month-day portion
        random_key = random.random()  # Generate a random secondary sort key
        emit(date, random_key, json.dumps(record['text']))

def emit(key, random_key, text):
    print(f"{key}\t{random_key}\t{text}")

if __name__ == "__main__":
    mapper()
