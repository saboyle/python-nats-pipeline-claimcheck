## Publish random data with payloads of desired size to NATS message queue.
# Allow size of message to be set via parameters.
# Allow wait between messages to be set via parameters.
# Initially implement without claim check / storage of data outside of message as V1 then later with claim check as V2.

import asyncio
import json

from nats.aio.client import Client as NATS
import asyncpg

NATS_HOST = 'localhost'
NATS_PORT = '4222'

queues = {'raw_data': 'p1.s0',
          'with_claim': 'p1.s1',
          'restored': 'p1.s2'}


async def pipeline(loop):
    #####################
    # Connection to NATS
    #####################
    nc = NATS()
    await nc.connect(f"{NATS_HOST}:{NATS_PORT}", loop=loop)
    pgconn = await asyncpg.connect(user='postgres', password='password', database='postgres', host='127.0.0.1')

    async def store_claim(claim_id, data):
        print('In store_claim', claim_id, data)
        await pgconn.execute('''INSERT INTO claims (claim_id, payload) VALUES ($1, $2);''', claim_id,  data)

    #####################
    # Message Handlers
    #####################
    async def mh_s1(msg):
        print("In mh_s1")
        idata = json.loads(msg.data.decode('utf-8'))
        rdata = {'uid': str(idata['uid']), 'claim_id': idata['uid']}
        print(json.dumps(rdata))

        await store_claim(str(idata['uid']), json.dumps({'data': idata['data']}))

        print("publishing to p1.s1")
        await nc.publish("p1.s1", json.dumps(rdata).encode('utf-8'))

    ######################
    # Pipeline Creation
    ######################
    await nc.subscribe("p1.s0", cb=mh_s1)


if __name__ == '__main__':

    print("Constructing test pipeline - p2")

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(pipeline(event_loop))

    try:
        print('Run forever')
        event_loop.run_forever()
    finally:
        print('Closing')
