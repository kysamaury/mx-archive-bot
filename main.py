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
    "oh god no": "https://www.youtube.com/watch?v=DcqLAtdYfU0&pp=ygUWb2ggZ29kIG5vIGZuZiA%3D%3D",
    "mario sing and game rhythm 9": "https://www.youtube.com/watch?v=4LvyiLJh5pA&list=RD4LvyiLJh5pA&start_radio=1&pp=ygUnbWFyaW8gc2luZyBhbmQgZ2FtZSByaHl0aG0gOSBmbmY%3D",
    "i hate you": "https://www.youtube.com/watch?v=gHMCdfcpE7M&pp=ygUXaSBoYXRlIHlvdSBmbmY%3D",
    "paranoia": "https://klipy.com/gifs/marios-madness-fnf"
}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Mario's Madness v2"))
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

    for song_title, video_url in SONG_TRIGGERS.items():
        if song_title in content_lower:
            await message.channel.send(f"👀 **Did someone say `{song_title.title()}`?**\n{video_url}")
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
