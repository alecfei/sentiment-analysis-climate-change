#!/usr/bin/env python3

import sys
from collections import Counter

# Dictionary to store word counts
word_counts = Counter()

# Read word-count pairs from standard input
for line in sys.stdin:
    try:
        word, count = line.strip().split("\t")
        count = int(count)

        # Increment the count for the word
        word_counts[word] += count
    except ValueError:
        pass

# Get the top 10 most common words
top_words = word_counts.most_common(10)

# Output the top 10 words with their counts
for word, count in top_words:
    print("%s\t%d" % (word, count))
