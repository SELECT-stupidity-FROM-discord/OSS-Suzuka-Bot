from xml.etree.ElementTree import ElementTree

import aiohttp
from bs4 import BeautifulSoup
from utils.helpers.functions import executor


class AnimeNewsRepresenter:
    def __init__(
        self, 
        title: str, 
        description: str, 
        image: str, 
        url: str
    ) -> None:
        self.title = title
        self.description = description
        self.image = image
        self.url = url
        
    @executor()
    @staticmethod
    def get_image(html: str) -> str:
        soup = BeautifulSoup(html, 'lxml')
        image = soup.find('p', {'align': 'center'}).find('img')['data-src']
        return image

    @classmethod
    def from_information(cls, title: str, image: str, description: str, url: str) -> 'AnimeNewsRepresenter':
        return cls(title, description, image, url)

    @classmethod
    async def construct(cls, root: ElementTree, session: aiohttp.ClientSession) -> 'AnimeNewsRepresenter':
        item = root.find('channel/item')
        title = item.find('title').text # type: ignore
        description = item.find('description').text # type: ignore
        url = item.find('guid').text # type: ignore
        html = await session.get(url) # type: ignore
        try:
            partial_image = await cls.get_image(await html.text())
            image = "https://www.animenewsnetwork.com/" + partial_image
        except (AttributeError, TypeError):
            image = "https://i.imgur.com/rKCYWIp.png"
        return cls(title, description, image, url) # type: ignore

    def to_json(self) -> dict:
        return {
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'url': self.url
        }

    def __repr__(self) -> str:
        return f'<AnimeNewsRepresenter title={self.title} description={self.description} image={self.image} url={self.url}>'
    