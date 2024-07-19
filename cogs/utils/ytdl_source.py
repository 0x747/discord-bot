import yt_dlp as youtube_dl
import discord
import asyncio
from discord import FFmpegPCMAudio
import os

ytdl_options = {'format': 'm4a/bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a',}]
               }
ffmpeg_options = {'options': '-vn'}

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

downloaded_filename = os.path.join('yt/', '%(extractor)s-%(id)s-%(title)s.%(ext)s') 

ytdl_format_options = {
    'format': 'bestaudio/best',
    'writethumbnail': True, 
    'outtmpl': downloaded_filename,
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
previous_filename = ""
channel_name = ""

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        
        for file in os.listdir("yt"):
            try:
                os.remove('yt/' + file)
            except Exception as e:
                print(e)

        loop = loop or asyncio.get_event_loop()

        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        except Exception as e:
            print(e)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        
        channel_name = data['uploader']

        filename = data['url'] if stream else ytdl.prepare_filename(data)

        return cls(FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
