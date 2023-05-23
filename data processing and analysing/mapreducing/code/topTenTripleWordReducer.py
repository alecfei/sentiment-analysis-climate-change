#!/usr/bin/env python3

import sys
from collections import Counter

# Dictionary to store triple word counts
triple_word_counts = Counter()

# Read triple-word count pairs from standard input
for line in sys.stdin:
    try:
        triple_word, count = line.strip().split("\t")
        count = int(count)

        # Increment the count for the triple word
        triple_word_counts[triple_word] += count
    except ValueError:
        pass

# Get the top 10 most common triple words
top_triple_words = triple_word_counts.most_common(10)

# Output the top 10 triple words with their counts
for triple_word, count in top_triple_words:
    print("%s\t%d" % (triple_word, count))
