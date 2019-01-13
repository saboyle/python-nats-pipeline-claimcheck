# Publish random data with payloads of desired size to NATS message queue.
# Allow size of message to be set via parameters.
# Allow wait between messages to be set via parameters.
# Initially implement without claim check / storage of data outside of message as V1 then later with claim check as V2.

import asyncio
import random
import json

from nats.aio.client import Client as NATS


NUM_MESSAGES = 1000
MSG_SIZE =  99999  # Bytes - Works
# MSG_SIZE = 1000000  # Bytes - Exceeds maximum

PAUSE = 1/100    # In Seconds

NATS_HOST = 'localhost'
NATS_PORT = '4222'

queues = {'raw_data': 'p1.s0'}


async def pub_random(loop):
    nc = NATS()
    await nc.connect(f"{NATS_HOST}:{NATS_PORT}", loop=loop)

    if nc.last_error:
        print("ERROR received from NATS: ", nc.last_error)
    else:
        print('Submitting random requests')
        for i in range(100):
            jdata = {"data": list(random.getrandbits(8) for _ in range(0, MSG_SIZE))}
            await nc.publish(queues['raw_data'], json.dumps(jdata).encode('utf-8'))
            # await asyncio.wait(PAUSE)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(pub_random(event_loop))