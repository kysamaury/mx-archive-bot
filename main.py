import os
import threading
from flask import Flask
import discord
from discord.ext import commands
from discord import app_commands

# --- KEEP-ALIVE SERVER FOR 24/7 HOSTING ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

# --- DISCORD BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True  # Required to read chat messages for song names

bot = commands.Bot(command_prefix="!", intents=intents)

# Add all your song triggers here!
SONG_TRIGGERS = {
    "its a me": ",
    "starman slaughter": "",
    "all stars": "https://www.youtube.com/watch?v=gHMCdfcpE7M&pp=ygUXaSBoYXRlIHlvdSBmbmY%3D",
    "all star": "https://klipy.com/gifs/marios-madness-fnf",
    "so cool": "https://cdn.discordapp.com/attachments/1538562192952266783/1538568501940322315/so_cool.gif?ex=6a832714&is=6a81d594&hm=dd18a7bcc141fa0210b2c3ca5bfbe31386f8af12610e060833f4e875db34f1c2&",
    "mario sing and game rhythm 9": "https://cdn.discordapp.com/attachments/1538562192952266783/1538567838879457320/msagr.gif?ex=6a832675&is=6a81d4f5&hm=e83769ac2b6b4c0ad4f85c703fc8491185b528f9490226573b4735d46ea1fdba&",
    "nourishing blood":
    "alone":
    "oh god no":
    "ogn":
    "i hate you":
    "ihy":
    "thalassophobia":
    "apparition":
    "last course":
    "dark forest":
    "bad day":
    "day out":
    "dictator":
    "race traitors":
    "race traitor":
    "no hope":
    "no party":
    "piracy":
    "golden land":
    "paranoia":
    "paranoid":
    "too late":
    "overdue":
    "powerdown":
    "demise":
    "promotion":
    "abandoned":
    "the end":
    "unbeatable":
    "you cannot beat us":
    
}

@bot.event
async def on_ready():
    # Set status to Do Not Disturb (red dot) with custom playing text
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game(name="Mario's Madness v2")
    )
    print(f'Logged in as {bot.user}!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# --- CHAT LISTENER FOR SONG TRIGGERS ---
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    for song_title, gif_url in SONG_TRIGGERS.items():
        if song_title in content_lower:
            embed = discord.Embed(
                title=f"👀 Did someone say {song_title.title()}?",
                color=discord.Color.red()
            )
            embed.set_image(url=gif_url)
            await message.channel.send(embed=embed)
            break

    await bot.process_commands(message)
# --- EMBED BUILDER COMMAND ---
class EmbedBuilderModal(discord.ui.Modal, title="Custom Embed Builder"):
    embed_title = discord.ui.TextInput(label="Title", placeholder="Enter embed title...", required=True)
    description = discord.ui.TextInput(label="Description", style=discord.TextStyle.paragraph, placeholder="Enter main text/description here...", required=True)
    color_hex = discord.ui.TextInput(label="Color (Hex Code)", placeholder="e.g. #FF5733", required=False)
    image_url = discord.ui.TextInput(label="Main Image URL", placeholder="https://example.com/image.png (Optional)", required=False)
    thumbnail_url = discord.ui.TextInput(label="Thumbnail Image URL", placeholder="https://example.com/thumb.png (Optional)", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        color_val = discord.Color.blurple()
        if self.color_hex.value:
            hex_str = self.color_hex.value.lstrip('#')
            try:
                color_val = discord.Color(int(hex_str, 16))
            except ValueError:
                pass

        embed = discord.Embed(title=self.embed_title.value, description=self.description.value, color=color_val)
        if self.image_url.value:
            embed.set_image(url=self.image_url.value)
        if self.thumbnail_url.value:
            embed.set_thumbnail(url=self.thumbnail_url.value)
        embed.set_footer(text=f"Created by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="embedbuilder", description="Create a custom embed")
async def embedbuilder(interaction: discord.Interaction):
    await interaction.response.send_modal(EmbedBuilderModal())

# Start keep-alive server and run bot
keep_alive()
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
