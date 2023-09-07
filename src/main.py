from discord.ext import commands
from discord import app_commands
import discord

import os
from dotenv import load_dotenv


load_dotenv()


class MyBot(commands.Bot):

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        await self.load_extension("cogs.tts")

    async def on_ready(self) -> None:
        print("Now ready!")
    

bot = MyBot(intents=discord.Intents.all(), command_prefix="sam!")


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))