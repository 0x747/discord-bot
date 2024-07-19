import discord 
from discord.ext import commands
import asyncio
import datetime

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix=[">"], intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has logged in at {datetime.datetime.now()}")

extensions = ["cogs.member", "cogs.admin"]

async def main() -> None:
    async with bot:
        for extension in extensions:
            await bot.load_extension(extension)

        await bot.start("")

asyncio.run(main())