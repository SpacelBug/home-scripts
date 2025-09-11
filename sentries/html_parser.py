import requests
from bs4 import BeautifulSoup
import os


def find_audio_urls(page_url: str) -> list[str]:
    """
    Функция для поиска всех аудио ссылок на странице
    """
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    audio_urls = []

    for audio_tag in soup.find_all('audio'):
        if audio_tag.has_attr('src'):
            audio_urls.append(audio_tag['src'])
        for source_tag in audio_tag.find_all('source'):
            if source_tag.has_attr('src'):
                audio_urls.append(source_tag['src'])

    return audio_urls
