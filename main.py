from array import array
import os
from pytube import YouTube
from googleapiclient.discovery import build
from moviepy.editor import *
import re

def obter_links_videos_api  (api_key, playlistId):
    youtube = build('youtube', 'v3', developerKey=api_key)
    playlist_items = youtube.playlistItems().list(part='contentDetails', playlistId=playlistId, maxResults=50).execute()
    
    print(playlist_items)

    links_videos = []

    for item in playlist_items['items']:
        video_id = item['contentDetails']['videoId']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        links_videos.append(video_link)

    return links_videos

def baixar_trecho_do_meio(url, destino, index, inicio=0, fim=0, confirmacao='n'):
   
    try:
        print(F'Baixa o vídeo url: {url}, destino: {destino} e index: {index}')
        yt = YouTube(url)

        # Baixa o vídeo completo
        print(F'Salvando o video na pasta: {destino}/{yt.title}.mp4')

        video_stream = yt.streams.filter(subtype='mp4', progressive=True, res='720p').first()
        novo_caminho = f'novo_nome_{index}.mp4'
        video_stream.download(output_path=destino, filename=novo_caminho)
        caminho_original = os.path.join(destino, novo_caminho)

        if confirmacao == 'n':
            # Calcula o tempo de início e fim para o trecho de x segundos a partir do meio
            meio = yt.length / 2
            inicio_trecho = meio - inicio
            fim_trecho = meio + fim

            # Corta o trecho do vídeo
            print(F'CORTANDO O VÍDEO')
            caminho_trecho = os.path.join(destino, f'cute_{index}.mp4')

            print(F'Caminho original {caminho_original}')
            video_clip = VideoFileClip(caminho_original).set_duration(yt.length)
            video_clip_subclip = video_clip.subclip(inicio_trecho, fim_trecho)
            video_clip_subclip.write_videofile(caminho_trecho, codec='libx264')
            print(f'Trecho de 2 segundos do meio do vídeo baixado: {caminho_trecho}')
        if confirmacao == 's':
            video_stream = yt.streams.filter(subtype='mp4', progressive=True, res='720p').first()
            novo_caminho = f'novo_nome_{index}.mp4'
            video_stream.download(output_path=destino, filename=novo_caminho)
            caminho_original = os.path.join(destino, novo_caminho)
            
    except Exception as e:   
        print(f"An exception occurred: {e}")


    print(f"________________________________________________________________________________")

def passar_playlist_ids (playlist=[]):
    playlistIds: array = playlist
    insercao = input("Digite o Id da playlist que você deseja baixar (se já houver adicionada todos os ids, digite 'prosseguir'): ")
    if insercao == 'prosseguir' and playlistIds == []:
        return 'sem playlists'
    
    if insercao == 'prosseguir':
        return playlistIds
    else: 
        playlistIds.append(insercao)
        print(playlistIds)
        return passar_playlist_ids(playlistIds)

def exec_all (): 
    if __name__ == "__main__":
        api_key = '<YOUR-API-KEY>'
        channel_id = '' # id do canal
        link_playlists = passar_playlist_ids() #id's das playlists
        links_videos= []
        
        for link_playlist in link_playlists:
            links_videos = links_videos + obter_links_videos_api(api_key, link_playlist)

        destino_videos = 'videos'

        if not os.path.exists(destino_videos):
            os.makedirs(destino_videos)

        confirmacao = input("Deseja baixar apenas os vídeos inteiros [s/n]: ")
        if confirmacao == 'n':
            inicio = int(input("Digite quantos segundos para antes do meio dos vídeo: "))
            fim = int(input("Digite quantos segundos para depois do meio dos vídeo: "))
            for indice, video_url in enumerate(links_videos):
                baixar_trecho_do_meio(video_url, destino_videos, indice, inicio, fim, confirmacao)
        if confirmacao == 's':
            for indice, video_url in enumerate(links_videos):
                baixar_trecho_do_meio(video_url, destino_videos, indice, inicio=0, fim=0, confirmacao=confirmacao) 

exec_all()
