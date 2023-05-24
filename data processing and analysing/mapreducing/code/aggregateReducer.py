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
                for i in range(min(len(records), 900)):
                    emit(current_date, records[i])

            current_date = date
            records = []

        records.append(text)

    if current_date:
        random.shuffle(records)
        for i in range(min(len(records), 900)):
            emit(current_date, records[i])

def emit(key, text):
    print(f"{key}\t{text}")

if __name__ == "__main__":
    reducer()
