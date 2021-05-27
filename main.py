import discord
from discord.ext import commands
from discord.ext.commands import bot
import os

bot = commands.Bot(command_prefix = "d ")

@bot.event
async def on_ready():
    print("Con vịt chạy lạch bà lạch bạch")

@bot.event
async def on_member_join(member):
    print(f'{member} đã gia nhập vào đàn vịt thế giới!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Thưa ngài chuồng vịt bị delay: {round(bot.latency * 1000)}ms.')

@bot.command()
async def chao(ctx):
    await ctx.send(f"Xin chào bạn vịt tên: {ctx.author.name}!")
    
bot.run('ODQ2NzQ5Njg5MDY3MzM5ODU2.YK0DGQ.PJxU6ARD3mMU9SlOZMdq0VPqHqc')
