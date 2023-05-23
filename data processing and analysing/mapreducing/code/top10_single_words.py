#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep
import json
import re

WORD_RE = re.compile(r"[\w']+")

class TopWordsMRJob(MRJob):
    def mapper(self, _, line):
        try:
            record = json.loads(line)
            text = record['text']
            words = re.findall(WORD_RE, text.lower())
            for word in words:
                yield word, 1
        except Exception as e:
            # Handle JSON parsing errors, if any
            pass

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer_init(self):
        self.top_words = []

    def reducer(self, word, counts):
        total_count = sum(counts)
        self.top_words.append((total_count, word))
        self.top_words = sorted(self.top_words, reverse=True)[:10]

    def reducer_final(self):
        for count, word in self.top_words:
            yield word, count

    def steps(self):
        return [
            MRStep(mapper=self.mapper, combiner=self.combiner,
                   reducer_init=self.reducer_init, reducer=self.reducer,
                   reducer_final=self.reducer_final)
        ]

if __name__ == '__main__':
    TopWordsMRJob.run()
