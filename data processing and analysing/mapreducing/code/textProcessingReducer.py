#!/usr/bin/env python3

import sys
import json

for line in sys.stdin:
    record = json.loads(line)
    if 'text' in record:
        date = record.get('date', '')  # Retrieve the "date" field
        processed_text = record['text']
        print(date, processed_text)
        
