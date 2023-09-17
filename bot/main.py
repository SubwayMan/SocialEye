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

class Viewer(discord.ui.View):
    def __init__(self, bot, elements):
        super().__init__()
        self.bot = bot
        self.left_button = discord.ui.Button(label="Previous", style=discord.ButtonStyle.blurple)
        self.right_button = discord.ui.Button(label="Next", style=discord.ButtonStyle.blurple)
        self.left_button.callback = self.left_callback
        self.right_button.callback = self.right_callback
        self.current_page = len(elements)-1
        self.elements = elements
        self.add_item(self.left_button)
        self.add_item(self.right_button)
        
    async def on_timeout(self):
        await self.message.edit(view=None)
        
    async def left_callback(self, interaction):
        self.current_page -= 1
        if self.current_page == 0:
            self.left_button.disabled = True
        else:
            self.left_button.disabled = False
            
        await interaction.response.edit_message(embed=self.elements[self.current_page], view=self)
        
    async def right_callback(self, interaction):
        self.current_page += 1
        if self.current_page == len(self.elements)-1:
            self.right_button.disabled = True
        else:
            self.right_button.disabled = False
            
        await interaction.response.edit_message(embed=self.elements[self.current_page], view=self)


def get_urls():
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
    return urls, timestamps
    
@bot.command()
async def test(ctx):
    await ctx.respond("https://storage.googleapis.com/dss-bucket/videos/Garfield%20Dancing%20to%20Happy.mp4")


@bot.command()
async def viewer(ctx):

    urls, timestamps = get_urls()
    embeds = []
  
    for i in range(len(urls)):
        converted_time = datetime.fromtimestamp(timestamps[i]).strftime("%Y-%m-%d %H:%M:%S")
        embed = discord.Embed(title=f"Viewer", description=f"See past captures." , color=0xffff00)
      
        embed.add_field(name=f"{converted_time}", value=urls[i])
        embed.set_footer(text="All times in UTC.")
        embeds.append(embed)
      
    await ctx.respond(" ", embed=embeds[-1], view=Viewer(bot, embeds))

@bot.command()
async def dingus(ctx):
  ctx.respond("dongus")

@bot.command()
async def recordings(ctx):
    urls, timestamps = get_urls()
    embed = discord.Embed(title="Recordings", description=f"The {len(urls)} most recent recordings.", color=0x00ff00)
    for i in range(len(urls)):
        converted_time = datetime.fromtimestamp(timestamps[i]).strftime("%Y-%m-%d %H:%M:%S")
        embed.add_field(name=f"{converted_time}", value=urls[i], inline=False)

    embed.set_footer(text="All times in UTC.")
    await ctx.respond(" ", embed=embed)
  
bot.run(token)