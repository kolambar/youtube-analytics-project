import os
import json
from googleapiclient.discovery import build


api_key: str = os.getenv('API_KEY')

class Channel:
    """Класс для ютуб-канала"""

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id # делаем id полем класса

        # поле со всей информацией о канале в виде большого словаря
        self.response = self.youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=channel_id
        ).execute()

        # Обработка полученного ответа на нужные словари
        channel = self.response['items'][0]
        snippet = channel['snippet']
        statistics = channel['statistics']

        # создание нужных нам полей с информацией
        self.title = snippet['title'] # название канала
        self.description = snippet['description'] # описание канала
        self.subscribers = int(statistics['subscriberCount']) # количество подписчиков
        self.video_count = int(statistics['videoCount']) # количество видео
        self.view_count = int(statistics['viewCount']) # количество просмотров
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id # ссылка на канал

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        '''
        сложение подписчиков
        :param other:
        :return:
        '''
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        return self.subscribers - other.subscribers

    def __lt__(self, other):
        '''
        сравнение количества подписчиков
        :param other:
        :return:
        '''
        return self.subscribers < other.subscribers

    def __le__(self, other):
        return self.subscribers <= other.subscribers

    def __gt__(self, other):
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        return self.subscribers >= other.subscribers

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.response, indent=4, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        '''
        возвращающий объект для работы с YouTube API
        '''
        return cls.youtube

    def to_json(self, file_name):
        '''
        сохраняет в файл значения атрибутов экземпляра `Channel`.
        есть больлшое поле response оно нужно в методе, но содержет много второстепенной информации. можно пропускать
        '''
        fields = vars(self)
        instance_info = {}
        for fild_name, fild_value in fields.items():
            instance_info[fild_name] = fild_value
        with open(file_name, "w", encoding='utf-8') as write_file:
            json.dump(instance_info, write_file, separators=(',', ': '), indent=4, ensure_ascii=False)
