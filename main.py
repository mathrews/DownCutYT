import os
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
from googleapiclient.discovery import build

def obter_links_videos_api  (api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    playlist_items = youtube.playlistItems().list(part='contentDetails', playlistId=channel_id).execute()

    links_videos = []

    for item in playlist_items['items']:
        video_id = item['contentDetails']['videoId']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        links_videos.append(video_link)

    return links_videos

def baixar_trecho_do_meio(url, destino):
    yt = YouTube(url)
    
    # Calcula o tempo de início e fim para o trecho de 2 segundos a partir do meio
    meio = yt.length / 2
    inicio_trecho = max(meio - 1, 0)  # Começa 1 segundo antes do meio
    fim_trecho = min(meio + 1, yt.length)  # Termina 1 segundo após o meio

    # Baixa apenas o trecho desejado
    video_stream = yt.streams.filter(subtype='mp4', progressive=True).first()
    caminho_trecho = os.path.join(destino, f'{yt.title}_trecho.mp4')
    video_stream.download(output_path=destino, filename=f'{yt.title}_trecho', start=inicio_trecho, end=fim_trecho)

    print(f'Trecho de 2 segundos do meio do vídeo baixado: {caminho_trecho}')

if __name__ == "__main__":
    api_key = 'AIzaSyAux-INzqgqv1hEffmIx9s1lOdydq_tEwk'  # Substitua pela sua chave de API do YouTube
    channel_id = 'ID_DO_CANAL'  # Substitua pelo ID do canal desejado
    links_videos = obter_links_videos_api(api_key, channel_id)

    destino_videos = 'C:\\Downloads'

    if not os.path.exists(destino_videos):
        os.makedirs(destino_videos)

    for video_url in links_videos:
        baixar_trecho_do_meio(video_url, destino_videos)