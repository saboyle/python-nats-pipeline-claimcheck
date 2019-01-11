# Python Nats Pipeline Claimcheck

## Overview

Project to explore the implementation of the claim check EIP pattern using NATs ref. (https://www.enterpriseintegrationpatterns.com/patterns/messaging/StoreInLibrary.html)

NATs message size is restricted to a 1MB message size.  The size of messages will impact performance.  

There options available:
* Split the payload into multiple messages.
* Re-architect to use smaller payloads.
* Use a persistent store to keep all non-essential reference data out of the message and pass 
on a reference within the message pipeline to enable retrieval as necessary during later 
pipeline stages. (Claim Check pattern 346 EIP)

## Questions

* What factors should be considered?
* How does the use of the claim check affect performance?
* How can be implementation of the claim check be designed for maximum performance?
* Options to validate payloads to protect the content store.

## Outline

1. Select toolset options (Python 3.x, NATS, AsyncIO, Uvloop, asyncpg, schematics, redis/postgresql)
2. Design abstract canonical pipeline - minimal example to support analysis.
3. Analyse (code / benchmark)
