import aiohttp


class ElasticHandler(object):
    def __init__(self, addr, index, entity):
        self.address = f'{addr}/{index}/{entity}'
        self.active = bool(addr)

    async def add_data(self, data: dict):
        async with aiohttp.ClientSession() as session:
            await session.post(self.address, json=data, headers={'Content-Type': 'application/json'})
