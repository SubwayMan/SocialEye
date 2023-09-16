import discord
import os
from discord.ext import commands

# initialize bot
token = os.environ["BOT_TOKEN"]
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

@bot.command()
async def test(ctx):
  await ctx.respond("hello")

bot.run(token)