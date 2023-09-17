import discord
import os
from datetime import datetime
from discord.ext import commands
import requests
import random
import re

# initialize bot
token = os.environ["BOT_TOKEN"]
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

@bot.command()
async def test(ctx):
  await ctx.respond("https://storage.googleapis.com/dss-bucket/videos/Garfield%20Dancing%20to%20Happy.mp4")

@bot.command()
async def recordings(ctx):
  url = "https://discord-security-system.subwayman.repl.co/video-index"
  req = requests.get(url)
  items = req.json()["items"]
  urls = []
  for item in items:
    if item.endswith(".mp4"):
      urls.append(f"https://storage.googleapis.com/dss-bucket/{item}")
      
  urls.sort()
  timestamps = []
  for url in urls:
    timestamps.append(int(re.search(r"\d+", url).group(0)))

  embed = discord.Embed(title="Recordings", description=f"The {len(urls)} most recent recordings.", color=0x00ff00)
  for i in range(len(urls)):
    converted_time = datetime.fromtimestamp(timestamps[i]).strftime("%Y-%m-%d %H:%M:%S")
    embed.add_field(name=f"{converted_time}", value=urls[i], inline=False)
    
  await ctx.respond(" ", embed=embed)



bot.run(token)