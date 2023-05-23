#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep
import json
import re

WORD_RE = re.compile(r"[\w']+")

class TopDoubleWordsMRJob(MRJob):
    def mapper(self, _, line):
        try:
            record = json.loads(line)
            text = record['text']
            words = re.findall(WORD_RE, text.lower())
            for i in range(len(words) - 1):
                double_word = ' '.join(words[i:i+2])
                yield double_word, 1
        except Exception as e:
            # Handle JSON parsing errors, if any
            pass

    def combiner(self, double_word, counts):
        yield double_word, sum(counts)

    def reducer_init(self):
        self.top_double_words = []

    def reducer(self, double_word, counts):
        total_count = sum(counts)
        self.top_double_words.append((total_count, double_word))
        self.top_double_words = sorted(self.top_double_words, reverse=True)[:10]

    def reducer_final(self):
        for count, double_word in self.top_double_words:
            yield double_word, count

    def steps(self):
        return [
            MRStep(mapper=self.mapper, combiner=self.combiner,
                   reducer_init=self.reducer_init, reducer=self.reducer,
                   reducer_final=self.reducer_final)
        ]

if __name__ == '__main__':
    TopDoubleWordsMRJob.run()
