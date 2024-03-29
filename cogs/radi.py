import radiko
from discord.ext import commands

from audio import audiosource
from cogs import voice


class RadiCog(voice.VoiceCore):

    radi = radiko.Client()

    def __init__(self, bot):
        super().__init__(bot)

    @commands.group()
    async def radiko(self, ctx):
        if ctx.author.bot:
            return
        if ctx.invoked_subcommand is not None:
            return

        text_channel = ctx.channel
        user_voice = ctx.author.voice
        voice_channel = None
        if user_voice != None:
            voice_channel = user_voice.channel

        args = ctx.message.content.split(' ')

        if len(args) == 1:
            await self.show_station(text_channel)
        else:
            args = args[1:]
            if voice_channel == None:
                await ctx.send("ボイスチャンネルから呼んでね")
            await self.enter_voice_channel(voice_channel)
            self.stop_source(voice_channel)
            radi_source = audiosource.RadiSource(args[0])
            await self.play_source(voice_channel, radi_source)

    @classmethod
    async def show_station(cls, channel):
        msg = "放送局一覧\n"
        for idx, station in enumerate(RadiCog.radi.get_stations()):
            msg += "[{idx}] {id} : {name}\n".format(idx=idx, id=station.id, name=station.name)
            msg += "    {title}  {ft} ~ {to}\n\n".format(title=station.get_on_air().title,
                                                         ft=station.get_on_air().ft.strftime("%H:%M"),
                                                         to=station.get_on_air().to.strftime("%H:%M"))
        await channel.send(msg)


def setup(bot):
    bot.add_cog(RadiCog(bot))
