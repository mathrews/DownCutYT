import os
import requests
from bs4 import BeautifulSoup
from pytube import YouTube

def obter_links_videos(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links_videos = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'watch?v=' in href:
            video_id = href.split('watch?v=')[1]
            video_link = f'https://www.youtube.com/watch?v={video_id}'
            links_videos.append(video_link)

    return links_videos

def baixar_trecho_meio_video(url, destino):
    yt = YouTube(url)
    
    # Obtém a stream de maior resolução disponível
    video_stream = yt.streams.get_highest_resolution()

    if video_stream:
        # Baixa o trecho do meio do vídeo
        caminho_salvar = os.path.join(destino, f'{yt.title}_trecho_meio.mp4')
        video_stream.download(output_path=destino, filename=f'{yt.title}_trecho_meio')
        print(f'Trecho do meio do vídeo baixado: {caminho_salvar}')
    else:
        print(f'Não foi possível encontrar uma stream para o vídeo: {url}')

if __name__ == "__main__":
    url_canal = 'https://www.youtube.com/@ujelbplus'  # Substitua pela URL do canal desejado
    links_videos = obter_links_videos(url_canal)

    destino_videos = 'C:\\Teteus\\DownCutYT\\videos'

    if not os.path.exists(destino_videos):
        os.makedirs(destino_videos)

    for video_url in links_videos:
        baixar_trecho_meio_video(video_url, destino_videos)
