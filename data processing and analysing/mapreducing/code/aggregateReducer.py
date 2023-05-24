#!/usr/bin/env python3

import sys
import random
import json

def reducer():
    current_date = None
    records = []

    for line in sys.stdin:
        date, random_key, text = line.strip().split('\t')
        if current_date != date:
            if current_date:
                random.shuffle(records)
                for i in range(min(len(records), 20)):
                    emit(records[i])

            current_date = date
            records = []

        records.append(text)

    if current_date:
        random.shuffle(records)
        for i in range(min(len(records), 20)):
            emit(records[i])

def emit(text):
    output = json.loads(text)
    print(json.dumps(output))

if __name__ == "__main__":
    reducer()

