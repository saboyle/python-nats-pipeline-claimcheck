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

    #######################
    # Claim store interface
    #######################
    async def store_claim(claim_id, data):
        pgconn = await asyncpg.connect(user='postgres', password='password', database='postgres', host='127.0.0.1')
        await pgconn.execute('''INSERT INTO claims (claim_id, payload) VALUES ($1, $2);''', claim_id,  data)
        await pgconn.close()

    async def retrieve_claim(claim_id):
        pgconn = await asyncpg.connect(user='postgres', password='password', database='postgres', host='127.0.0.1')
        select_stmt = await pgconn.prepare('''SELECT payload FROM claims WHERE claim_id = $1''')

        rec = await select_stmt.fetchrow(claim_id, timeout=10)
        await pgconn.close()
        return rec

    #####################
    # Message Handlers
    #####################
    async def mh_s1(msg):
        data = json.loads(msg.data.decode('utf-8'))
        logger.info('Processing {}'.format(data["uid"]))
        logger.debug('In mh_s1 with {}'.format(data))
        idata = json.loads(msg.data.decode('utf-8'))
        rdata = {'uid': str(idata['uid']), 'claim_id': idata['uid']}

        await store_claim(str(idata['uid']), json.dumps({'data': idata['data']}))
        await nc.publish("p1.s1", json.dumps(rdata).encode('utf-8'))


    async def mh_s2(msg):
        logger.debug('In mh_s2 with {}'.format(msg.data.decode('utf-8')))
        idata = json.loads(msg.data.decode('utf-8'))
        claim = await retrieve_claim(idata['uid'])
        response = json.dumps({'uid': idata['uid'], 'data': json.loads(claim['payload'])['data']})
        logger.debug('Response in mh_s2 {}'.format(response))
        await nc.publish("p1.s2", response.encode('utf-8'))


    async def mh_s3(msg):
        logger.debug('In mh_s3 with {}'.format(msg.data.decode('utf-8')))

    ######################
    # Pipeline Creation
    ######################
    await nc.subscribe("p1.s0", cb=mh_s1)
    await nc.subscribe("p1.s1", cb=mh_s2)
    await nc.subscribe("p1.s2", cb=mh_s3)


if __name__ == '__main__':

    import logging

    logging.basicConfig(format='%(asctime)s, %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logging.getLogger("asyncio").setLevel(logging.INFO)

    print("Constructing test pipeline - p2")

    event_loop = asyncio.get_event_loop()
    # event_loop.set_debug(True)
    event_loop.run_until_complete(pipeline(event_loop))

    try:
        print('Run forever')
        event_loop.run_forever()
    finally:
        print('Closing')
