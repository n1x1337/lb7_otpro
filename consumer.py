import os
import asyncio
import aiohttp
from lxml import html
import pika
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
TIMEOUT = 10

def connect_to_rabbitmq():
    parameters = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='links')
    return connection, channel

async def fetch_and_extract_links(url, session):
    print(f"Обработка: {url}")
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to fetch {url}")
                return []
            html_content = await response.text()
            tree = html.fromstring(html_content)
            links = tree.xpath("//a[@href]")
            extracted_links = []
            for link in links:
                href = link.attrib['href']
                full_url = urljoin(url, href)
                extracted_links.append(full_url)
                print(f"Найденные ссылки: {full_url}")
            return extracted_links
    except Exception as e:
        print(f"Ошибка обработки {url}: {e}")
        return []

async def consumer():
    connection, channel = connect_to_rabbitmq()
    async with aiohttp.ClientSession() as session:
        while True:
            method_frame, _, body = channel.basic_get(queue='links')
            if body:
                url = body.decode('utf-8')
                channel.basic_ack(method_frame.delivery_tag)
                links = await fetch_and_extract_links(url, session)
                for link in links:
                    channel.basic_publish(exchange='', routing_key='links', body=link)
            else:
                await asyncio.sleep(TIMEOUT)
                print(f"Очередь пуста в течение {TIMEOUT} секунд, завершаем работу...")
                break
    connection.close()

if __name__ == "__main__":
    asyncio.run(consumer())
