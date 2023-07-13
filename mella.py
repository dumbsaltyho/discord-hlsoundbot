import discord
from discord.ext import commands
from HlSoundLibs import HlSoundGen as HlSoundGen
from HlSoundLibs import (BotErrorTooManyArgs as BotErrorTooManyArgs, BotErrorTtsTypeDoesNotExist as BotErrorTtsTypeDoesNotExist)

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='v.', intents=intents, status=discord.Status.dnd, activity=discord.Activity(name="in the sewer", type=1))

@client.command()
async def tts(ctx, ttsType: str, *, message: str):
    """ hl audio mashing """
    try:
        soundBuilder = HlSoundGen.soundBuilder(ttsType, message)
    except BotErrorTooManyArgs:
        print("too many args, user probably used the command wrong.")
        await ctx.send("command formatting error, please see v.ttshelp")
        return
    except BotErrorTtsTypeDoesNotExist:
        print("fileLocation does not exist, ttsType is wrong.")
        await ctx.send("one or more ttsType does not exist, please see v.ttshelp")
        return

    if ctx.voice_client == None:
        await ctx.send(file=discord.File(soundBuilder))
    else:
        sound_file = discord.FFmpegPCMAudio(soundBuilder)
        ctx.voice_client.play(source=sound_file, after=None)
        await ctx.send(file=discord.File(soundBuilder))

@client.command()
async def stop(ctx):
    """ stops current playback """
    await ctx.voice_client.stop()

@client.command()
async def leave(ctx):
    """ dc from da vc """
    await ctx.voice_client.disconnect()

@client.command()
async def ttshelp(ctx):
    """ send useless help informatin """
    ttsHelpEmbed = discord.Embed(type="rich", title="v.ttshelp",description="v.ttshelp")
    ttsHelpEmbed.add_field(name="How to use the command", value="v.tts requires at least 2 arguments: ttsType and message. ttsType determines what type of soundfile will be \
        used, and message is a word from the list of a given type (full types and lists can be found at https://salty.gay/vox/ or in the Half-Life sounds folder) Any words after \
        the ttsType will be used, so a message can be almost as long as you want.\n\n ttsType `mixed` (or `m`) allows you to use multiple types at once, but requires each word \
        to be prefaced with ttsType: (ie. `vox:freeman`).\n\n Try running a command like `v.tts m vox:freeman vox:is hgrunt:shit!`.")
    await ctx.send(embed=ttsHelpEmbed)

@client.command()
async def join(ctx):
    """ c to da vc """
    channel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name, bitrate=64000)
    await discord.VoiceChannel.connect(channel)

@client.command()
async def quit(ctx):
    ''' correctly quit the bot '''
    if str(ctx.author.id) == "144781413558910976":
        await client.close()

client.run(token)