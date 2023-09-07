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
        self._channels: list[discord.TextChannel] = []

    async def tts(self, text: str) -> bytes:
        async with self._session.post(
            f"{ENDPOINT}/audio_query",
            params={
                "text": text,
                "speaker": 1,
            },
        ) as aqr:
            data = await aqr.json()
            data["outputStereo"] = True
            data["outputSamplingRate"] = 48000
            async with self._session.post(
                f"{ENDPOINT}/synthesis",
                params={
                    "speaker": 1,
                },
                json=data,
            ) as res:
                return await res.read()

    @app_commands.command(description="読み上げを開始します。")
    async def join(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        voice_client = await interaction.user.voice.channel.connect(cls=VoiceClient)
        track = await voice_client.source(await self.tts("接続しました"), opus=False)
        track.play()
        self._channels.append(interaction.channel)
        await interaction.followup.send("Hello")

    @app_commands.command(description="読み上げを終了します")
    async def leave(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await interaction.guild.voice_client.disconnect()
        self._channels.remove(interaction.channel)
        await interaction.followup.send("読み上げを終了しました。")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if message.channel in self._channels:
            track = await message.guild.voice_client.source(
                await self.tts(message.content), opus=False
            )
            track.play()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TTSCog(bot))
