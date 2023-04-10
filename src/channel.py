import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    __API_KEY: str = os.getenv('YT_API_KEY')
    # создать специальный объект для работы с API
    __youtube = build('youtube', 'v3', developerKey=__API_KEY)

    @classmethod
    def get_video_info(cls, video_id: str) -> dict:
        """Метод для получения информации о видео из Youtube по его id"""

        video_response = cls.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=video_id
                                                     ).execute()
        return video_response

    @classmethod
    def get_service(cls):
        return cls.__youtube

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscribers_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.views_count = self.channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        """Свойство для обращения к приватному атрибуту __channel_id"""
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name: str) -> None:
        """Запись информации о канале в file_name.json"""
        with open(file_name, 'w') as json_file:
            json.dump(self.channel, json_file, ensure_ascii=False)

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, other) -> int:
        """Сложение классов по количеству подписчиков"""
        return int(self.subscribers_count) + int(other.subscribers_count)

    def __sub__(self, other) -> int:
        """Разность классов по количеству подписчиков"""
        return int(self.subscribers_count) - int(other.subscribers_count)

    def __gt__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        return int(self.subscribers_count) > int(other.subscribers_count)

    def __ge__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        return int(self.subscribers_count) >= int(other.subscribers_count)

    def __lt__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        return int(self.subscribers_count) < int(other.subscribers_count)

    def __le__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        return int(self.subscribers_count) <= int(other.subscribers_count)

    def __eq__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        return int(self.subscribers_count) == int(other.subscribers_count)
