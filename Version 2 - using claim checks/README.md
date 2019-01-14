# ClaimCheck pipeline example

## Overview

Implementation of a pipeline using the ClaimCheck integration pattern.

## Setup

* Run 5 terminals
1. python p2_server.py
2. python ./utils/nats-wiretap.py p2.s0
3. python ./utils/nats-wiretap.py p2.s1
4. python ./utils/nats-wiretap.py p2.s2
5. python p2_random_publisher.py

The output from Terminal 2 and Terminal 4 should be identical (although the ordering of the dict fields
may differ).

## Notes

* This version can be improved by either re-using the pg connection or using a connection pool.
* asyncpg connections can be configured to automatically marshal/de-marshal to a number of 
formats including json.  This would simplify the code.

## Future
* Refactor to use asyncpg connection pool.
* Refactor to use asyncpg automated marshal/de-marshal.