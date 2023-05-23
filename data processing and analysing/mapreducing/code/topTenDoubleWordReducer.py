#!/usr/bin/env python3

import sys
from collections import Counter

# Dictionary to store double word counts
double_word_counts = Counter()

# Read double-word count pairs from standard input
for line in sys.stdin:
    try:
        double_word, count = line.strip().split("\t")
        count = int(count)

        # Increment the count for the double word
        double_word_counts[double_word] += count
    except ValueError:
        pass

# Get the top 10 most common double words
top_double_words = double_word_counts.most_common(10)

# Output the top 10 double words with their counts
for double_word, count in top_double_words:
    print("%s\t%d" % (double_word, count))
