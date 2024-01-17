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
    url_canal = 'https://www.youtube.com/@ujelbplus'  # Substitua pela URL do canal desejado
    links_videos = obter_links_videos(url_canal)

    destino_videos = 'C:\\Downloads'

    if not os.path.exists(destino_videos):
        os.makedirs(destino_videos)

    for video_url in links_videos:
        baixar_trecho_do_meio(video_url, destino_videos)