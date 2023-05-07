import json
from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""
    path = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=path)

    def __init__(self, channel_id: str) -> None:
        """
        Инициализатор, который позволяет по id канала подтянуть все необходимые о нём данные.
        """
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.parsed_string = json.dumps(self.channel, indent=2, ensure_ascii=False)
        self.title = self.channel["items"][0]["snippet"]["title"]

        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = 'https://www.youtube.com/channel/' + self.channel["items"][0]["id"]
        self.subscribers = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

        self.channel_info = {'channel_id': self.channel_id, 'title': self.title, 'description': self.description,
                         'url': self.url, 'subscribers': self.subscribers, 'video_count': self.video_count,
                         'view_count': self.view_count}

    @property
    def channel_id(self):
        """
        Ограничитель прав на изменения в поле channel_id
        """
        return self.__channel_id

    def print_info(self) -> None:
        """
        Выводит в консоль всю информацию о канале.
        """
        print(self.parsed_string)

    @classmethod
    def get_service(cls):
        """
        Позволяет получить объект для работы с API вне класса
        """
        return cls.youtube

    def to_json(self, filename):
        """
        Запись кратких сведений о канале в файл формата json
        """
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.channel_info, file, ensure_ascii=False)

