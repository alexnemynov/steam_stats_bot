import aiohttp
import asyncio
from bs4 import BeautifulSoup
from config_data.config import load_config, Config
from fake_useragent import UserAgent


async def get_soup(session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        return soup


async def get_all_links() -> list[str]:
    config: Config = load_config()
    # print(config.steam_profiles)
    return config.steam_profiles


async def parse_page(session: aiohttp.ClientSession, url: str) -> int:
    async with session.get(url) as response:
        if response.status == 200:
            soup = await get_soup(session, url)
            username = soup.select_one('span.actual_persona_name').text.strip()
            hours = soup.select_one('div.recentgame_quicklinks.recentgame_recentplaytime div').text.strip()
            return f"<b>{username}</b> {hours}"


async def parse() -> None:
    ua = UserAgent()
    fake_ua = {'user_agent': ua.random}
    connector = aiohttp.TCPConnector(limit=200)
    links = await get_all_links()

    async with aiohttp.ClientSession(headers=fake_ua, connector=connector) as session:

        tasks = [asyncio.create_task(parse_page(session, link)) for link in links]
        result = await asyncio.gather(*tasks)
        print(result)
        return '\n'.join(result)


# asyncio.run(parse())