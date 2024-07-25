#!/usr/bin/env python

import sys
import json

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} ../../metadata/*-test.jsonl >test-records.jsonl")
    sys.exit(1)

for fn in sys.argv[1:]:
    with open(fn) as infile:
        for line in infile:
            rec = json.loads(line)
            rec['prediction'] = {}
            print(json.dumps(rec))

            
