import discord 
from discord.ext import commands
import random
import configparser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
from discord import FFmpegPCMAudio
from .utils import ytdl_source
from .utils import IMDbScraper
import datetime

local_dir = "music"
contents = os.listdir(local_dir)
scraper = IMDbScraper.IMDb_Scraper()

song_list = []
music_folders = os.listdir("music")

for folder in music_folders:
    songs = os.listdir(f"music/{folder}")
    for song in songs:
        song_list.append(folder + "/" + song)
       
    
class Member(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Member Cog Loaded.")
    
    @commands.command()
    async def flip(self, ctx) -> None:
        """ Flips a coins and sends the result """

        await ctx.send(random.choice(["Heads", "Tails"]))

    @commands.command()
    async def random(self, ctx, lower_bound: int = 0, upper_bound: int = 100) -> None:
        """ Sends a random number between the lower (inclusive) and upper bound (inclusive) """

        await ctx.send(random.randint(lower_bound, upper_bound))

    @commands.command()    
    async def ls(self, ctx, dir = "music") -> None:
        """ Lists the files in a given directory """

        dir_tree = ""
        index = 0
        song_list = []
        
        for folder in music_folders:
            dir_tree += "\u001b[0;41m" + folder + ":\u001b[0m\n"
            songs = os.listdir(f"music/{folder}")
            for song in songs:
                song_list.append(folder + "/" + song)
                index += 1
                dir_tree +=  "\t" + f"\u001b[0;33m[{index}]\u001b[0m  \u001b[0;36m{song}\u001b[0m" + f"\n"
            await ctx.send(f'```ansi\n{dir_tree}\n{len(dir_tree)}```')
            dir_tree = ""
        # for file in os.listdir(dir):
        #     index += 1
        #     list += str(index) + ". " + file + "\n"

    @commands.command()
    async def join(self, ctx):
        """ Joins a voice channel """

        channel = ctx.message.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
    
    @commands.command()        
    async def play(self, ctx, *, name: str) -> None:
        """ Plays audio from the local filesystem """

        
        local = "music"
        if(name.isnumeric()):
            path = song_list[int(name) - 1]
        else:
            path = process.extractOne(name, song_list, scorer=fuzz.partial_ratio)[0]
        
        await self.join(ctx)
        global local_dir
        if(ctx.voice_client.is_playing() and path in song_list):
            ctx.voice_client.stop()

        absolute_path = local_dir + "/" + path
        
        source = discord.PCMVolumeTransformer(FFmpegPCMAudio(absolute_path))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
        
        # Extracts cover art and metadata from and audio file using ffmpeg
        try:
            os.system("cd music && ffmpeg -i " + path.replace("'", "\\'").replace(" ", "\ ") + " -an -vcodec copy ../cover.png -y && ffmpeg -i "+ path.replace("'", "\\'").replace(" ", "\ ") + " -f ffmetadata ../metadata.ini -y") 
        except:
            print("[Metadata Extraction]:", e)

        # path = local_dir + "/" + path
        
        # source = discord.PCMVolumeTransformer(FFmpegPCMAudio(path))
        # ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        with open("metadata.ini", 'r+') as fd:
            contents = fd.readlines()
            contents.insert(1, "[metadata]\n")
            fd.seek(0)  
            fd.writelines(contents)

        c = configparser.ConfigParser()
        c.read("metadata.ini")
        
        metadata = c['metadata']  # get the metadata section

        # create a new dictionary with lowercase keys
        new_metadata = {key.lower(): value for key, value in metadata.items()}

        title = new_metadata.get("title", path).split(";")[0]
        artist = new_metadata.get("artist", "N/A").split(";")[0]
        year = new_metadata.get("year") or new_metadata.get("date", "N/A").split(";")[0]
        album = new_metadata.get("album", "N/A").split(";")[0]

        try:
            song_embed = discord.Embed(title=f'Now Playing: {title}', timestamp=datetime.datetime.now())
            song_embed.add_field(name="Artist", value=artist, inline=True)
            song_embed.add_field(name="Year", value=year, inline=True)
            song_embed.add_field(name="Album", value=album, inline=False)
            song_embed.set_thumbnail(url="attachment://cover.png")
            print(title, artist, year, album)
            file = discord.File("cover.png", filename="cover.png")
            await ctx.send(file=file, embed=song_embed)
        except Exception as e:
            print(e)

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await ytdl_source.YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        thumbnail = ''
        for filename in os.listdir("yt"):
            if filename.endswith(('.webp', '.jpg', '.jpeg', '.png')):
                thumbnail = filename
                break
        print("Thumbnail name:", thumbnail)
        
        yt_embed = discord.Embed(title=f'Now Playing: {player.title}', description=f"Requested by {ctx.message.author.mention}", timestamp=datetime.datetime.now(), color=0xFF0000)
        file = discord.File("yt/" + thumbnail, filename=thumbnail)
        yt_embed.set_thumbnail(url="attachment://" + thumbnail)
        
        await ctx.send(file=file, embed=yt_embed)

    @play.before_invoke
    @yt.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(embed=discord.Embed(title="You are not connected to a voice channel."))
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command()
    async def imdb(self, ctx, *, query) -> None:
        """ Fetches IMDb metadata for a given motion picture """
                
        message = await ctx.send(embed=discord.Embed(title="Searching...", description="This may take a few seconds."))
        response = scraper.scrape(query)
        
        movie_embed = discord.Embed(title = f'{response["title"]} ({response["year"]})', 
                                    url = response["imdb_url"], 
                                    description = response["plot"],
                                    color = 0xE0B416,
                                    timestamp=datetime.datetime.now()) 
        movie_embed.set_image(url=response["poster_url"])
        movie_embed.add_field(name="Genre", value=scraper.to_string(response["genre"]), inline=True)
        movie_embed.add_field(name="IMDb Rating", value=response["imdb_rating"], inline=True)
        movie_embed.add_field(name="Age Rating", value=response["age_rating"], inline=True)
        movie_embed.add_field(name="Duration", value=scraper.format_runtime(response["runtime"]), inline=True)
        movie_embed.add_field(name="Language", value=scraper.to_string(response["languages"]), inline=True)
        movie_embed.add_field(name="Directed by", value=scraper.to_string(response["directors"]), inline=True) 
        movie_embed.add_field(name="Cast", value=scraper.to_string(response["cast"]), inline=False)            

        await message.delete()
        await ctx.send(embed=movie_embed)

    @commands.command()
    async def pause(self, ctx) -> None:
        """ Pauses the audio output from bot """

        if (ctx.voice_client.is_playing):
            await ctx.voice_client.pause()
            #paused_embed = discord.Embed(title="Audio Paused", description=f'{ctx.message.author.mention} paused the audio.', color = 0xfc751b)
        # else:
        #     await ctx.send("Audio is already paused.")
            #paused_embed = discord.Embed(title="Audio is already paused.", color = 0xfc751b)

        #await ctx.send(embed=paused_embed)

    @commands.command()
    async def resume(self, ctx) -> None:
        """ Resumes the audio output from bot """

        if (ctx.voice_client.is_paused):
            await ctx.voice_client.resume()

        #     resumed_embed = discord.Embed(title="Audio Resumed", description=f'{ctx.message.author.mention} resumed the audio.', color = 0x0bea2d)
        # else:
        #     #resumed_embed = discord.Embed(title="Audio is already playing.", color = 0x0bea2d)

        # await ctx.send(embed=resumed_embed)
    
    @commands.command()
    async def stop(self, ctx) -> None:
        """ Stops the audio playback """

        await ctx.voice_client.stop()

        #await ctx.send(embed = discord.Embed(title="Playback Stopped", description=f"{ctx.message.author.mention} stopped the audio playback.", color = 0xfc751b))
    
    @commands.command()
    async def disconnect(self, ctx) -> None:
        """ Disconnects the bot from voice channel """

        await ctx.voice_client.disconnect()
        await ctx.voice_client.cleanup()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

        if payload.emoji.name == '📌' and reaction.count >= 1:
            pinned_channel = self.bot.get_channel()
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            
            pinned_message_embed = discord.Embed(title=f'{message.author.display_name} in #{channel.name}', description=f'{message.content} [{message.jump_url}]')
            pinned_message_embed.set_footer(text=f"Pinned by {payload.member.name}")

            await pinned_channel.send(embed=pinned_message_embed)
            await channel.send(f"Message pinned in [{message.jump_url}]")

    

async def setup(bot) -> None:
    await bot.add_cog(Member(bot))