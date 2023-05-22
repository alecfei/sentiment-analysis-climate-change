#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep
import json

class TypeCountMRJob(MRJob):
    def mapper(self, _, line):
        try:
            record = json.loads(line)
            type_value = record['type']
            yield type_value, 1
        except Exception as e:
            # Handle JSON parsing errors, if any
            pass

    def reducer(self, key, values):
        yield key, sum(values)

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer)
        ]

if __name__ == '__main__':
    TypeCountMRJob.run()
