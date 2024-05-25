import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup

async def get_page(session, url):
    try:
#пытаемся отправить запрос для получения кода
        async with session.get(url) as response:
#получение кода html сайта
            return await response.text()
#в случае если не получиться
    except aiohttp.ClientConnectorError:
        return ""


async def parse_page(html):
#объект для парсинга сайта
    soup = BeautifulSoup(html, 'html.parser')
#получаем ссылки, которые в html коде имеют теги <a> с атрибутом href
    links = [a.get('href') for a in soup.find_all('a', href = True) if 'http' in a.get('href')]
    return links

async def craw(session, url):
    try:
#получение html кода сайта
        html = await get_page(session, url)
#получение ссылок из кода
        links = await parse_page(html)
        print(f"Found {len(links)} links on {url}")
#сохранение ссылок в файл links.txt
        async with aiofiles.open("links.txt", 'a') as file:
            for link in links:
                await file.write(link + '\n')
    except Exception as e:
        print(f"Error crawling {url}: {e}")

async def main(urls):
#создание сессии http клиента
    async with aiohttp.ClientSession() as session:
#создание задач для обработки каждой ссылки
        tasks = [craw(session, url) for url in urls]
        await asyncio.gather(*tasks)

urls = [
    'https://regex101.com/',
    'https://docs.python.org/3/this-url-will-404.html',
    'https://www.nytimes.com/guides/',
    'https://www.mediamatters.org/',
    'https://1.1.1.1/',
    'https://www.politico.com/tipsheets/morning-money',
    'https://www.bloomberg.com/markets/economics',
    'https://www.ietf.org/rfc/rfc2616.txt']

asyncio.run(main(urls))


