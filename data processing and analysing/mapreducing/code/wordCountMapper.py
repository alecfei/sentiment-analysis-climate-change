#!/usr/bin/env python3

import sys
import json

# Read input from standard input
for line in sys.stdin:
    # Parse the JSON object
    try:
        record = json.loads(line)
    except ValueError as e:
        # Skip invalid JSON records
        continue

    # Extract the "type" field
    if "type" in record:
        record_type = record["type"]

        # Emit key-value pair for the "type" field
        print(f"{record_type}\t1")
