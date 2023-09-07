from aiohttp import ClientSession
from discord import app_commands
import discord
from discord.ext import commands

from dextbird import VoiceClient
from os import getenv


ENDPOINT: str = getenv("ENDPOINT")


class TTSCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._session = ClientSession()

    async def tts(self, text: str) -> bytes:
        async with self._session.post(f"{ENDPOINT}/audio_query", params={
            "text": text,
            "speaker": 1,
        }) as aqr:
            data = await aqr.json()
            data["outputStereo"] = False
            data["outputSamplingRate"] = 48000
            async with self._session.post(f"{ENDPOINT}/synthesis", params={
                "speaker": 1,
            }) as res:
                return await res.read()

    @app_commands.command()
    async def join(self, interaction: discord.Interaction) -> None:
        voice_client = await interaction.user.voice.channel.connect(cls=VoiceClient)
        track = await voice_client.source(await self.tts("接続しました"))
        track.play()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TTSCog(bot))