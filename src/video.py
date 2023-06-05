from googleapiclient.discovery import build
import os


api_key: str = os.getenv('API_KEY')


class Video:
    """Класс для ютуб-видео"""

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id # делаем id полем класса

        # поле со всей информацией о видео в виде большого словаря
        response = self.youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()

        # Обработка полученного ответа на нужные словари
        try:
            video = response['items'][0]
        except IndexError:
            self.title = None
            self.like_count = None
            self.view_count = None
            self.url = None
        else:
            snippet = video['snippet']
            statistics = video['statistics']

            # создание нужных нам полей с информацией
            self.title = snippet['title'] # название видео
            self.like_count = int(statistics['likeCount']) # количество лайков
            self.view_count = int(statistics['viewCount']) # количество просмотров
            self.url = 'https://www.youtube.com/watch?v=' + self.__video_id # ссылка на видео

    def __repr__(self):
        return f'id {self.__video_id}/название {self.title}/количество лайков {self.video_count}/количество просмотров {self.view_count}/ссылка {self.url}'

    def __str__(self):
        return self.title

class PLVideo(Video):
    """Класс для ютуб-видео с привязкой к плейлисту"""
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __repr__(self):
        return f'название {self.title}/количество лайков {self.video_count}/количество просмотров {self.view_count}/ссылка {self.url}/id плейлиста {self.playlist_id}'
