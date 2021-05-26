import discord
from discord.ext import commands
import youtube_dl
import os

client = commands.Bot(command_prefix = "v ")

@client.event
async def on_ready():
    print("Con vịt chạy lạch bà lạch bạch")

@client.event
async def on_member_join(member):
    print(f'{member} đã gia nhập vào đàn vịt thế giới!')

@client.command()
async def ping(ctx):
    await ctx.send(f'Thưa ngài chuồng vịt bị delay: {round(client.latency * 1000)}ms.')

@client.command()
async def chao(ctx):
    await ctx.send(f"Xin chào bạn vịt tên: {ctx.author.name}!")

client.run('ODQ2NzQ5Njg5MDY3MzM5ODU2.YK0DGQ.PJxU6ARD3mMU9SlOZMdq0VPqHqc')
