#!/usr/bin/env python3

import sys

current_type = None
current_count = 0

# Read input from standard input
for line in sys.stdin:
    # Parse the input
    record_type, count = line.strip().split('\t')

    # Convert count to integer
    count = int(count)

    # If it's the same type, increment the count
    if current_type == record_type:
        current_count += count
    else:
        # If it's a new type, print the previous type and count
        if current_type:
            print(f"{current_type}\t{current_count}")
        # Update the current type and count
        current_type = record_type
        current_count = count

# Print the last type and count
if current_type:
    print(f"{current_type}\t{current_count}")

