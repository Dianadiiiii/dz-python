import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def get_page(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except aiohttp.ClientConnectorError:
        return ""

async def parse_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/wiki/')]

async def len_page(session, start, end):
    queue = [(start, [start])] #очередь
    seen = set([start]) #уникальные посещенные сайты 
    while queue:
        url, path = queue.pop(0) #извлекаем первый элемент из очереди
        html = await get_page(session, f'https://en.wikipedia.org{url}')
        for link in await parse_links(html): #получаем html код 
            if link == end: #найдена последняя статья 
                return path + [link]
            if link not in seen: #если раннее не посещали эту ссылку 
                seen.add(link)
                queue.append((link, path + [link]))

async def main(start_url, end_url):
    async with aiohttp.ClientSession() as session:
        path = await len_page(session, start_url, end_url)
        if path:
            print(f'Длина пути: {len(path)}')
        else:
            print('Путь не найден')

start = '/wiki/2007%E2%80%9308_Scottish_League_Cup'
end = '/wiki/Philosophy'
asyncio.run(main(start, end))
