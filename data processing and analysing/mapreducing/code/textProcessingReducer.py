#!/usr/bin/env python3

import sys
import json

for line in sys.stdin:
    try:
        record = json.loads(line)
        date = record['date']
        text = record['texts']
        
        output = {"date": date, "texts": text}
        print(json.dumps(output))
    
    except ValueError as e:
        # Handle any JSON decoding errors
        continue


