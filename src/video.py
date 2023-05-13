# coding=utf-8
from googleapiclient.discovery import build
import json
import os

path = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=path)


class Video:

    def __init__(self, video_id):
        """
        Инициализатор, который позволяет по id видео подтянуть все необходимые о нём данные
        """
        self.video_id = video_id
        self.videos = youtube.videos().list(id=self.video_id, part='snippet, statistics').execute()
        self.title = self.videos['items'][0]['snippet']['title']
        self.video_url = 'https://www.youtube.com/watch?v=' + self.videos['items'][0]['id']
        self.views_count = self.videos['items'][0]['statistics']['viewCount']
        self.likes_count = self.videos['items'][0]['statistics']['likeCount']

        self.video_info = {'video_id': self.video_id, 'title': self.title, 'video_url': self.video_url,
                           'views_count': self.views_count,
                           'likes_count': self.likes_count}

    def __str__(self):
        """
        Возвращает строку с названием видео
        """
        return self.title

    def __repr__(self):
        """
        Выводит краткую информацию о видео
        """
        return print(f'Название видео: {self.title}\n'
                     f'Ссылка на видео: {self.video_url}\n'
                     f'Количество просмотров: {self.views_count}\n'
                     f'Количество лайков: {self.likes_count}')

    def print_info(self) -> None:
        """
        Выводит информацию о видео в формате словаря
        в json-подобном формате с отступами
        """
        print(json.dumps(self.videos, indent=2, ensure_ascii=False))


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        """
        Инициализатор, который позволяет по id видео и id плейлиста подтянуть все необходимые данные
        о плейлисте и видео
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlists = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                      part='contentDetails',
                                                      maxResults=50,).execute()
        self.videos = youtube.videos().list(id=self.video_id, part='snippet, statistics').execute()


# video1 = Video('9lO06Zxhu88')  # '9lO06Zxhu88' - это id видео из ютуб
# video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
# video2.__repr__()
