#!/usr/bin/env python

import sys
import json

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <records.jsonl> [<records2.jsonl> ...] >test-records.jsonl")
    sys.exit(1)

for fn in sys.argv[1:]:
    with open(fn) as infile:
        for line in infile:
            rec = json.loads(line)
            rec['ground_truth'] = {fld: val for fld, val in rec.items() if fld.startswith('dc.')}
            rec['prediction'] = {}
            for fld in [fld for fld in rec if fld.startswith('dc.')]:
                del rec[fld]
            print(json.dumps(rec))

            
