import os
from pytube import YouTube
from googleapiclient.discovery import build
from moviepy.video.io.VideoFileClip import VideoFileClip

def obter_links_videos_api  (api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    playlist_items = youtube.playlistItems().list(part='contentDetails', playlistId='PLwdnFmzXKgfDpr-pVfxOV_dNJuLzFn8RD').execute()

    links_videos = []

    for item in playlist_items['items']:
        video_id = item['contentDetails']['videoId']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        links_videos.append(video_link)

    return links_videos

def baixar_trecho_do_meio(url, destino, fps=30):
    yt = YouTube(url)

    # Baixa o vídeo completo
    caminho_original = os.path.join(destino, f'{yt.title}_original.mp4')
    video_stream = yt.streams.filter(res='720p', subtype='mp4', progressive=True).first()
    video_stream.download(output_path=destino)

    # Calcula o tempo de início e fim para o trecho de x segundos a partir do meio
    meio = yt.length / 2
    inicio_trecho = max(meio - 2, 0)  # Começa x segundo antes do meio
    fim_trecho = min(meio + 3, yt.length)  # Termina x segundo após o meio

    # Corta o trecho do vídeo
    caminho_trecho = os.path.join(destino, f'{yt.title}_trecho.mp4')
    try:
        video_clip = VideoFileClip(f'{yt.title}_original.mp4')
        video_clip_subclip = video_clip.subclip(inicio_trecho, fim_trecho)
        video_clip_subclip.write_videofile(caminho_trecho, fps=fps, codec="libx264", audio_codec='aac', threads=4, verbose=False)
        print(f'Trecho de 2 segundos do meio do vídeo baixado: {caminho_trecho}')
        
        # Exclui o vídeo original
        os.remove(caminho_original)
    except Exception as e:
        print(f'Erro ao processar o vídeo: {e}')


if __name__ == "__main__":
    api_key = 'AIzaSyAux-INzqgqv1hEffmIx9s1lOdydq_tEwk'
    channel_id = 'UCbqyhIVG2wd9DX6aoHW_6rw'
    links_videos = obter_links_videos_api(api_key)

    destino_videos = 'C:\\Videos-UJELB+'

    if not os.path.exists(destino_videos):
        os.makedirs(destino_videos)

    for video_url in links_videos:
        baixar_trecho_do_meio(video_url, destino_videos)