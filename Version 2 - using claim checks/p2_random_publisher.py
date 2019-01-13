# Publish random data with payloads of desired size to NATS message queue.
# Allow size of message to be set via parameters.
# Allow wait between messages to be set via parameters.
# Initially implement without claim check / storage of data outside of message as V1 then later with claim check as V2.

import asyncio
import random
import json
import uuid

from nats.aio.client import Client as NATS
import asyncpg


NUM_MESSAGES = 10
MSG_SIZE = 10
# MSG_SIZE =  99999  # Bytes - Works
# MSG_SIZE = 1000000  # Bytes - Exceeds maximum

PAUSE = 1/100    # In Seconds

NATS_HOST = 'localhost'
NATS_PORT = '4222'

queues = {'raw_data': 'p1.s0',
          'with_claim': 'p1.s1',
          'restored': 'p1.s2'}


async def random_data(loop):
    # TODO: REUSE NATS and PG CONNECTIONS - REFACTOR
    nc = NATS()
    await nc.connect(f"{NATS_HOST}:{NATS_PORT}", loop=loop)
    pgconn = await asyncpg.connect(user='postgres', password='password',
                                 database='postgres', host='127.0.0.1')

    if nc.last_error:
        print("ERROR received from NATS: ", nc.last_error)
    else:
        print('Submitting random requests')
        for i in range(NUM_MESSAGES):

            uid  = str(uuid.uuid4())
            data = list(random.getrandbits(8) for _ in range(0, MSG_SIZE))

            await nc.publish(queues['raw_data'], json.dumps({"data": data, "uid": uid}).encode('utf-8'))

    await pgconn.close()

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(random_data(event_loop))