import discord
import shutil
import os
import youtube_dl
from discord.ext import commands
from discord.utils import get
from bot import client


class Voice(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice1 = get(client.voice_clients, guild=ctx.guild)

        if voice1 is not None:
            return await voice1.move_to(channel)

        await channel.connect()

        await ctx.send(f"Nghệ sĩ vịt đã tham gia vào kênh: {channel}!")

    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"Nghệ sĩ vịt đã ngắt kết nối với kênh: {channel}!")
        else:
            await ctx.send("Tao có ở kênh nào đâu, mày định cho tao đi đâu về đâu!")

    @commands.command(aliases=['p'])
    async def play(self, ctx, *url: str):
        print("Yêu cầu đã được chấp nhận bởi vịt!")
        channel = ctx.message.author.voice.channel
        voice1 = get(client.voice_clients, guild=ctx.guild)

        if voice1 is not None:
            await voice1.move_to(channel)

        try:
            await channel.connect()
        except:
            print("Nghệ sĩ vịt đã ở trong kênh!")

        def checkqueue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                    print("first file =" + first_file)
                except:
                    print("Mở thêm nhạc đi mấy thằng loz!")
                    queues.clear()
                    return
                main_location = os.path.dirname(
                    os.path.realpath("./Queue"))
                print("main location = " + main_location)
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                print("song path = " + song_path)
                if length != 0:
                    print("Nghệ sĩ vịt đã biểu diễn xong, cho nghỉ tí rồi hát tiếp cho nhé\n")
                    print(f"Tiếp theo là ca khúc mang tên: {still_q}")
                    song_exists = os.path.isfile("song.mp3")
                    if song_exists:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')
                    voicenew.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: checkqueue())
                    voicenew.source = discord.PCMVolumeTransformer(voicenew.source)
                    voicenew.source.volume = 0.15
                else:
                    queues.clear()
                    return
            else:
                queues.clear()
                print("Hát xong rồi, mở thêm nhạc đi mấy thằng loz!")

        song_exists = os.path.isfile("song.mp3")
        try:
            if song_exists:
                os.remove('song.mp3')
                queues.clear()
                print("Bùng hàng hả mày!")
        except PermissionError:
            await ctx.send("Từ đang hát bài khác rồi!")
            print("exception error")
            return

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                print("Removed old Queue Folder")
                shutil.rmtree(Queue_folder)
        except:
            print("No old queue folder")

        await ctx.send("Chờ tí, chờ tí...")

        voicenew = get(client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': './song.mp3',
            'postprocessors': [{
                'key': "FFmpegExtractAudio",
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        song_search = " ".join(url)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("downloading audio now...\n")
            ydl.download([f"ytsearch1:{song_search}"])

        voicenew.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: checkqueue())
        voicenew.source = discord.PCMVolumeTransformer(voicenew.source)
        voicenew.source.volume = 0.15

        print("playing song successfully")
        await ctx.send(f"Vịt đang hát bài: ")

    @commands.command()
    async def pause(self, ctx):
        voice2 = get(client.voice_clients, guild=ctx.guild)

        if voice2 and voice2.is_playing():
            voice2.pause()
            await ctx.send("Vịt đã tạm dừng hát!")
        elif voice2.is_paused():
            voice2.resume()
            await ctx.send("Vịt đã tiếp tục hát!")
        else:
            await ctx.send("Tao có hát đâu mày! Bỏ nghề rồi")

    @commands.command()
    async def skip(self, ctx):
        voice3 = get(client.voice_clients, guild=ctx.guild)
        queues.clear()
        if voice3 and voice3.is_playing():
            voice3.stop()
            await ctx.send("Đây đây sang bài mới rồi!")
        else:
            await ctx.send("Đã mở nhạc đâu thằng hâm này")

    global queues
    queues = {}

    @commands.command(aliases=["q", "qu", "que"])
    async def queue(self, ctx, *url: str):
        queue_infile = os.path.isdir("./Queue")
        if queue_infile is False:
            os.mkdir("./Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        qlength = len(os.listdir(DIR))
        qlength += 1
        add_queue = True
        while add_queue:
            if qlength in queues:
                qlength += 1
            else:
                add_queue = False
                queues[qlength] = qlength
        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{qlength}.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': "FFmpegExtractAudio",
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        song_search = " ".join(url)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("downloading queue audio now...\n")
            ydl.download([f"ytsearch1:{song_search}"])
        await ctx.send("Vịt đã được trả tiền để hát bài này: " + str(qlength))

    @commands.command()
    async def reset(self, ctx):
        voice4 = get(client.voice_clients, guild=ctx.guild)
        try:
            voice4.stop()
        except:
            await ctx.send("Tao có hát gì đâu, nhưng")
        queues.clear()
        queue_infile = os.path.isdir("./Queue")
        if queue_infile:
            shutil.rmtree("./Queue")
        try:
            for filename in os.listdir('./'):
                if filename.endswith(".mp3"):
                    os.remove(filename)
        except:
            await ctx.send("Đã bỏ nghề do hát không ai nghe!")

    @commands.command(aliases = ["v", "vol"])
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Tính thuê mà không có phòng hát thì tao hát sao!")

        print(volume/100)

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Vịt đã hét tới mức: {volume}%")


def setup(client):
    client.add_cog(Voice(client))

