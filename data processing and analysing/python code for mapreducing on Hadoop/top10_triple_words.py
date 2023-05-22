#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep
import json
import re

WORD_RE = re.compile(r"[\w']+")

class TopTripleWordsMRJob(MRJob):
    def mapper(self, _, line):
        try:
            record = json.loads(line)
            text = record['text']
            words = re.findall(WORD_RE, text.lower())
            for i in range(len(words) - 2):
                triple_word = ' '.join(words[i:i+3])
                yield triple_word, 1
        except Exception as e:
            # Handle JSON parsing errors, if any
            pass

    def combiner(self, triple_word, counts):
        yield triple_word, sum(counts)

    def reducer_init(self):
        self.top_triple_words = []

    def reducer(self, triple_word, counts):
        total_count = sum(counts)
        self.top_triple_words.append((total_count, triple_word))
        self.top_triple_words = sorted(self.top_triple_words, reverse=True)[:10]

    def reducer_final(self):
        for count, triple_word in self.top_triple_words:
            yield triple_word, count

    def steps(self):
        return [
            MRStep(mapper=self.mapper, combiner=self.combiner,
                   reducer_init=self.reducer_init, reducer=self.reducer,
                   reducer_final=self.reducer_final)
        ]

if __name__ == '__main__':
    TopTripleWordsMRJob.run()
