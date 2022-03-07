import aiohttp


async def api() -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/tqbr/securities.json") as response:
            return (await response.json())["history"]["data"]
