#!/usr/bin/env python3

import sys
import json
import csv

csv_writer = csv.writer(sys.stdout)

for line in sys.stdin:
    try:
        record = json.loads(line)
        
        # Extract the date, text, and sentiment from the record
        date = record['date']
        text = record['texts']
        sentiment = record['sentiment']
        
        # Emit the CSV row with date, text, and sentiment
        csv_writer.writerow([date, text, sentiment])
    
    except ValueError as e:
        # Handle any JSON decoding errors
        continue

