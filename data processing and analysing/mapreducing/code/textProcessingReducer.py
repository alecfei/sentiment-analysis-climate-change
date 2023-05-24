#!/usr/bin/env python3

import sys
import json

current_date = None
processed_text = ""

for line in sys.stdin:
    try:
        key, value = line.strip().split('\t')
        
        if key == "date":
            # Update the current date
            current_date = value
        elif key == "word":
            # Concatenate the processed text
            processed_text += value + " "
    
    except ValueError as e:
        # Handle any value errors
        continue

# Emit the final output
if current_date:
    output = {"date": current_date, "text": processed_text.strip()}
    print(json.dumps(output))

