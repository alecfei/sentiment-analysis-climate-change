#!/usr/bin/env python3

import sys
import json

for line in sys.stdin:
    record = json.loads(line)
    if '_id' in record:
        del record['_id']
    if 'type' in record:
        del record['type']
    print(json.dumps(record))
