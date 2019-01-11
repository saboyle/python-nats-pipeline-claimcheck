import asyncio
import asyncpg
import uvloop

async def run():
    await purge()
    await insert()
    await select()

    await insert_invalid1()

async def insert():
    conn = await asyncpg.connect(user='postgres', password='password',
                                 database='postgres', host='127.0.0.1')

    values = await conn.execute('''INSERT INTO claims VALUES ('13eb9327-f40e-4ef1-8020-1c36af1b4b70', '{"name":"test"}');''' )
    print(values)
    await conn.close()

async def select():
    conn = await asyncpg.connect(user='postgres', password='password',
                                 database='postgres', host='127.0.0.1')

    values = await conn.fetch(
        '''SELECT * FROM claims;''')
    print(values)
    await conn.close()

async def purge():
    conn = await asyncpg.connect(user='postgres', password='password',
                                 database='postgres', host='127.0.0.1')

    values = await conn.execute(
        '''DELETE FROM claims;''')
    print(values)
    await conn.close()

async def insert_invalid1():
    conn = await asyncpg.connect(user='postgres', password='password',
                                 database='postgres', host='127.0.0.1')

    values = await conn.execute('''INSERT INTO claims VALUES ('13eb9327', '{"name":"test"}');''' )
    print(values)
    await conn.close()

if  __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())