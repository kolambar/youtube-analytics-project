import os
import isodate
from datetime import timedelta
from googleapiclient.discovery import build


# YouTube API ключ
api_key: str = os.getenv('API_KEY')

class PlayList:

    # Создание YouTube API клиентa
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:

        # Выполните запрос к YouTube API для получения информации о поейлисте
        self.playlist_id = playlist_id  # Идентификатор поейлиста
        response = self.youtube.playlists().list(id=playlist_id,
                                     part='contentDetails,snippet',
                                     maxResults=50,
                                     ).execute()

        playlist = response['items'][0]

        # Формирование полей экземпляра
        self.title = playlist['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id


    def get_video_list(self):
        '''
        вспомогательная функция для создания списка видео плейлиста
        :return список:
        '''
        # Получает список видео в плейлисте
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50, # максимум 50 шт
                                                       ).execute()

        # Извлекает идентификаторы видео из полученных данных.
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # Запрашивает дополнительную информацию о видео
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        return video_response


    @property
    def total_duration(self):
        '''
        Проходит циклом по списку видео и суммирует длительность каждого
        :return общая длительность:
        '''
        sum_of_duration = timedelta(hours=0)
        video_response = self.get_video_list()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            sum_of_duration += duration

        return sum_of_duration

    def show_best_video(self):
        '''
        Проходит циклом по списку видео и находит самое залайканное
        :return ссылку на видео:
        '''
        video_response = self.get_video_list()
        best_score = 0
        best_video = None

        for video in video_response['items']:
            like_count: int = int(video['statistics']['likeCount'])
            if like_count > best_score:
                best_score = like_count
                best_video = 'https://youtu.be/' + video['id']

        return best_video
