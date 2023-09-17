import discord
import os
from datetime import datetime
from discord.ext import commands
import requests
import random
import re
import sys

# initialize bot
token = os.environ["BOT_TOKEN"]
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

if "--prod" in sys.argv:
    HOME_URL = "https://discord-security-system-subwayman.replit.app"
else:
    HOME_URL = "https://discord-security-system.subwayman.repl.co"
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
        self.right_button.disabled = True
        
    async def on_timeout(self):
        await self.message.edit(view=None)
        
    async def left_callback(self, interaction):
        self.right_button.disabled = False
        self.current_page -= 1
        if self.current_page == 0:
            self.left_button.disabled = True
        else:
            self.left_button.disabled = False
            
        await interaction.response.edit_message(content=self.elements[self.current_page], view=self)
        
    async def right_callback(self, interaction):
        self.current_page += 1
        self.left_button.disabled = False
        if self.current_page == len(self.elements)-1:
            self.right_button.disabled = True
        else:
            self.right_button.disabled = False
            
        await interaction.response.edit_message(content=self.elements[self.current_page], view=self)


def get_urls():
    url = HOME_URL+"/video-index"
    req = requests.get(url)
    items = req.json()["items"]
    urls = []
    for item in items:
        if item.endswith(".mp4"):
            item = item.split("/")[-1]
            urls.append(HOME_URL+f"/video/{item}")
            
    urls.sort()
    urls = urls[:15]
    timestamps = []
    for url in urls:
        timestamps.append(int(re.search(r"\d+", url).group(0)))
    return urls, timestamps
    
@bot.command()
async def test(ctx):
    await ctx.respond("https://www.youtube.com/watch?v=k9IDvub7yoQ")


@bot.command()
async def viewer(ctx):

    urls, timestamps = get_urls()
    embeds = []  
    await ctx.respond(content=urls[-1], view=Viewer(bot, urls))

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