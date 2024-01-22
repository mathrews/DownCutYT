import os
from pytube import YouTube
from googleapiclient.discovery import build
from moviepy.editor import *
import re

def obter_links_videos_api  (api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    playlist_items = youtube.playlistItems().list(part='contentDetails', playlistId='PLwdnFmzXKgfDpr-pVfxOV_dNJuLzFn8RD').execute()

    links_videos = []

    for item in playlist_items['items']:
        video_id = item['contentDetails']['videoId']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        links_videos.append(video_link)

    return links_videos

def baixar_trecho_do_meio(url, destino, index):
   

    try:
        print(F'Baixa o vídeo url: {url}, destino: {destino} e index: {index}')
        yt = YouTube(url)

        # Baixa o vídeo completo
        print(F'Salvando o video na pasta: {destino}/{yt.title}.mp4')

        video_stream = yt.streams.filter(subtype='mp4', progressive=True, res='720p').first()
        novo_caminho = f'novo_nome_{index}.mp4'
        video_stream.download(output_path=destino, filename=novo_caminho)
        caminho_original = os.path.join(destino, novo_caminho)

       
        # Calcula o tempo de início e fim para o trecho de x segundos a partir do meio
        meio = yt.length / 2
        inicio_trecho = meio - 2
        fim_trecho = meio + 3

        # Corta o trecho do vídeo
        print(F'CORTANDO O VÍDEO')
        caminho_trecho = os.path.join(destino, f'{yt.title}_cute.mp4')

        print(F'Caminho original {caminho_original}')
        video_clip = VideoFileClip(caminho_original).set_duration(yt.length)
        video_clip_subclip = video_clip.subclip(inicio_trecho, fim_trecho)
        video_clip_subclip.write_videofile(caminho_trecho, codec='libx264')
        print(f'Trecho de 2 segundos do meio do vídeo baixado: {caminho_trecho}')
        
        # Exclui o vídeo original
        os.remove(caminho_original)
    except Exception as e:   
        print(f"An exception occurred: {e}")


    print(f"________________________________________________________________________________")


if __name__ == "__main__":
    api_key = 'AIzaSyAux-INzqgqv1hEffmIx9s1lOdydq_tEwk'
    channel_id = 'UCbqyhIVG2wd9DX6aoHW_6rw'
    links_videos = obter_links_videos_api(api_key)

    destino_videos = 'videos'

    if not os.path.exists(destino_videos):
        os.makedirs(destino_videos)

    for indice, video_url in enumerate(links_videos):
        baixar_trecho_do_meio(video_url, destino_videos, indice)