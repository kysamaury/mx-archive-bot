import os
import asyncio
import threading
from flask import Flask
import discord
from discord import app_commands
from discord.ext import commands

# --- KEEP-ALIVE FLASK SERVER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

# --- DISCORD BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- HELP COMMAND ---
@bot.tree.command(name="help", description="Learn how to use MX Archive")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="<:mxsmile:1538591783645220965> MX Archive - Help Menu",
        description="Here is everything you can do with MX Archive! <:mxflower:1538616023928799363>",
        color=discord.Color.red()
    )
    
    embed.add_field(
        name="• <:mx:1538614409902170212> - `/madness` commands",
        value=(
            "`/madness flipoff @user` - Flip off a user\n"
            "`/madness kill @user` - Kill a user\n"
            "`/madness laugh @user` - Laugh at a user\n"
            "*(More reaction commands coming soon! )*"
        ),
        inline=False
    )
    
    embed.add_field(
        name="• <:music:1538614127659061359> - Automatic Triggers (Chat)",
        value=(
            "- Mention song names in chat (example: `starman slaughter`, `all stars`, `its a me`) to play gif embeds!\n"
            "- Try saying `i hate mx` in chat if you dare... <:mxsmile:1538591783645220965>"
        ),
        inline=False
    )
    
    embed.add_field(
        name="• <:mushroome:1538614584435277996> - embeds",
        value="• Embed Builder for anything u want lol.",
        inline=False
    )
    
    embed.set_footer(text="MX Archive - Mario's Madness Bot")
    await interaction.response.send_message(embed=embed)

# --- MADNESS REACTION COMMANDS GROUP ---
class MadnessGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="madness", description="Mario's Madness interaction reactions")

madness_group = MadnessGroup()

@madness_group.command(name="flipoff", description="flip off an annoying user")
async def flipoff(interaction: discord.Interaction, target: discord.User):
    embed = discord.Embed(
        title=f"{interaction.user.display_name} flips off {target.display_name} <:fuckyoumx:1538591235927965726>",
        description="fuck you",
        color=discord.Color.red()
    )
    embed.set_image(url="https://i.pinimg.com/736x/d5/08/12/d5081271cdf82eb695611f101342db7b.jpg")
    await interaction.response.send_message(embed=embed)

@madness_group.command(name="kill", description="kill a user")
async def kill(interaction: discord.Interaction, target: discord.User):
    embed = discord.Embed(
        title=f"{interaction.user.display_name} kills {target.display_name} 💀💀",
        description="DIE BITCH",
        color=discord.Color.dark_red()
    )
    embed.set_image(url="https://i.pinimg.com/736x/bc/a7/35/bca735ecf4b651b7fabd80c5ea785ec4.jpg")
    await interaction.response.send_message(embed=embed)

@madness_group.command(name="laugh", description="laugh ur ass off at a user")
async def laugh(interaction: discord.Interaction, target: discord.User):
    embed = discord.Embed(
        title=f"{interaction.user.display_name} laughs at {target.display_name}!",
        description="LMAOAOOAOAO",
        color=discord.Color.gold()
    )
    embed.set_image(url="https://i.pinimg.com/736x/5f/e6/8c/5fe68c736527cba5a324626ec0943394.jpg")
    await interaction.response.send_message(embed=embed)

bot.tree.add_command(madness_group)

# --- SONG TRIGGERS ---
SONG_TRIGGERS = {
    "its a me": "https://cdn.discordapp.com/attachments/1538562192952266783/1538570637134659705/its-a-me.gif?ex=6a832911&is=6a81d791&hm=d5baba022c476c58ad57fa92f882a36f31034853d5dff746507e007273fe224f&",
    "it's-a me": "https://cdn.discordapp.com/attachments/1538562192952266783/1538570637134659705/its-a-me.gif?ex=6a832911&is=6a81d791&hm=d5baba022c476c58ad57fa92f882a36f31034853d5dff746507e007273fe224f&",
    "it's a me": "https://cdn.discordapp.com/attachments/1538562192952266783/1538570637134659705/its-a-me.gif?ex=6a832911&is=6a81d791&hm=d5baba022c476c58ad57fa92f882a36f31034853d5dff746507e007273fe224f&",
    "starman slaughter": "https://cdn.discordapp.com/attachments/1538562192952266783/1538571763284451488/starman.gif?ex=6a832a1d&is=6a81d89d&hm=180c763376acb2b4d1dce7ebd9a26bdedae9fef7982f05759b6dc6a31c4549c9&",
    "all stars": "https://cdn.discordapp.com/attachments/1538562192952266783/1538579080994099240/all-stars.gif?ex=6a8330ee&is=6a81df6e&hm=caa074d312050a922bdb876e70d2b75a3ed986e50f51d16260cf6f793aee69ee&",
    "all-stars": "https://cdn.discordapp.com/attachments/1538562192952266783/1538579080994099240/all-stars.gif?ex=6a8330ee&is=6a81df6e&hm=caa074d312050a922bdb876e70d2b75a3ed986e50f51d16260cf6f793aee69ee&",
    "all star": "https://cdn.discordapp.com/attachments/1538562192952266783/1538579673686999150/all-stars-2.gif?ex=6a83317b&is=6a81dffb&hm=009bc0e3707e30f0e4d5ea0f02401791a309c3d4219f408265300dfbbb268138&",
    "so cool": "https://cdn.discordapp.com/attachments/1538562192952266783/1538568501940322315/so_cool.gif?ex=6a832714&is=6a81d594&hm=dd18a7bcc141fa0210b2c3ca5bfbe31386f8af12610e060833f4e875db34f1c2&",
    "mario sing and game rhythm 9": "https://cdn.discordapp.com/attachments/1538562192952266783/1538567838879457320/msagr.gif?ex=6a832675&is=6a81d4f5&hm=e83769ac2b6b4c0ad4f85c703fc8491185b528f9490226573b4735d46ea1fdba&",
    "nourishing blood": "https://cdn.discordapp.com/attachments/1538562192952266783/1538577039521620118/nourishing-blood.gif?ex=6a832f07&is=6a81dd87&hm=9f76e749a19c85018551f9b43acbb73735a8a39cd46c456ec313b045db094a94&",
    "nourish blood": "https://cdn.discordapp.com/attachments/1538562192952266783/1538577039521620118/nourishing-blood.gif?ex=6a832f07&is=6a81dd87&hm=9f76e749a19c85018551f9b43acbb73735a8a39cd46c456ec313b045db094a94&",
    "alone": "https://cdn.discordapp.com/attachments/1538562192952266783/1544379073776717824/alone.gif?ex=6a984a98&is=6a96f918&hm=0bef7dcce04fdb526839e5233f42ec37bdbe7af38fe44b5bcf44344900243419&",
    "oh god no": "https://cdn.discordapp.com/attachments/1538562192952266783/1538570662778507344/oh-god-no.gif?ex=6a832917&is=6a81d797&hm=4bed85b274b3bc9629b4eb3a847abd6293535e14917c1940ad2206aeddcefa25&",
    "i hate you": "https://cdn.discordapp.com/attachments/1538562192952266783/1538571042958872707/i-hate-you.gif?ex=6a832971&is=6a81d7f1&hm=8ec57cb332484fdc6d01770b597a60e1855d97b523718bc889e055aa4b4f99be&",
    "i hate u": "https://cdn.discordapp.com/attachments/1538562192952266783/1538571042958872707/i-hate-you.gif?ex=6a832971&is=6a81d7f1&hm=8ec57cb332484fdc6d01770b597a60e1855d97b523718bc889e055aa4b4f99be&",
    "thalassophobia": "https://cdn.discordapp.com/attachments/1538562192952266783/1538571619893514330/thalassaphobia.gif?ex=6a8329fb&is=6a81d87b&hm=9109f505c83d27dc24daf9df7baf4d21f64dc3a20c7888ce79ce91ba42c7a9c0&",
    "apparition": "https://cdn.discordapp.com/attachments/1538562192952266783/1538576341899939920/apparition.gif?ex=6a832e61&is=6a81dce1&hm=05e99f2d2f8ae7eda7089ef62022dc70c0ff1b7f7334b8a270cd929cc6804366&",
    "last course": "https://cdn.discordapp.com/attachments/1538562192952266783/1538572792641880135/last-course.gif?ex=6a832b13&is=6a81d993&hm=27ee6e54e031c3d1ea3610a4ee2b1bd11f626f05cc5465e210f04ff95e6bf42d&",
    "dark forest": "https://cdn.discordapp.com/attachments/1538562192952266783/1538576092569538600/dark-forest.gif?ex=6a832e25&is=6a81dca5&hm=666306bfb51d53319370bd5716b0833aba545218aa41d8e1be12261b32bc696d&",
    "bad day": "https://cdn.discordapp.com/attachments/1538562192952266783/1538577767203999774/bad-day.gif?ex=6a832fb5&is=6a81de35&hm=13f360346131158fd12b4c9311e30372c323340d03a098f3c01778415cebaf7c&",
    "day out": "https://cdn.discordapp.com/attachments/1538562192952266783/1538577980752789645/day-out.gif?ex=6a832fe8&is=6a81de68&hm=fde2cd1ddc80281045abbaa9249fe56c6875cfc1337baadbeb2ec73fecde5831&",
    "dictators": "https://cdn.discordapp.com/attachments/1538562192952266783/1538578294423691327/dictator.gif?ex=6a833032&is=6a81deb2&hm=ba747fab5dceb8e99ce0fed8c8d8ab37d2f5cb7e5c83fddf891388e4bd0d33fe&",
    "dictator": "https://cdn.discordapp.com/attachments/1538562192952266783/1538578294423691327/dictator.gif?ex=6a833032&is=6a81deb2&hm=ba747fab5dceb8e99ce0fed8c8d8ab37d2f5cb7e5c83fddf891388e4bd0d33fe&",
    "race traitors": "https://cdn.discordapp.com/attachments/1538562192952266783/1538573362819768383/race-traitors.gif?ex=6a832b9b&is=6a81da1b&hm=37a88957ca526100f173f67c9d19718c889f55ad61b717e4423d706a478bebed&",
    "race traitor": "https://cdn.discordapp.com/attachments/1538562192952266783/1538573362819768383/race-traitors.gif?ex=6a832b9b&is=6a81da1b&hm=37a88957ca526100f173f67c9d19718c889f55ad61b717e4423d706a478bebed&",
    "no hope": "https://cdn.discordapp.com/attachments/1538562192952266783/1538573901091700869/no-hope.gif?ex=6a832c1b&is=6a81da9b&hm=c81009902dea388ab0330b18e981734d7b120ed508c7eca0d7b958420e12f526&",
    "no party": "https://cdn.discordapp.com/attachments/1538562192952266783/1538574841542610984/no-party.gif?ex=6a832cfb&is=6a81db7b&hm=c44ec259b55379839473a86497f484311eb71469c4d6256b97a40086ead3ac05&",
    "piracy": "https://cdn.discordapp.com/attachments/1538562192952266783/1538574841542610984/no-party.gif?ex=6a832cfb&is=6a81db7b&hm=c44ec259b55379839473a86497f484311eb71469c4d6256b97a40086ead3ac05&",
    "golden land": "https://cdn.discordapp.com/attachments/1538562192952266783/1538578988723863602/golden-land.gif?ex=6a8330d8&is=6a81df58&hm=07b99c671bd02407ccff2ed55bec845813dd0aa823dd64421efd3c85b0f4e6fe&",
    "paranoid": "https://cdn.discordapp.com/attachments/1538562192952266783/1538572322762657832/paranoia.gif?ex=6a832aa3&is=6a81d923&hm=b378de278400c4c4c519eedea61b343e39c4ae953703fbd5999a0caa4d3bb61e&",
    "paranoia": "https://cdn.discordapp.com/attachments/1538562192952266783/1538572322762657832/paranoia.gif?ex=6a832aa3&is=6a81d923&hm=b378de278400c4c4c519eedea61b343e39c4ae953703fbd5999a0caa4d3bb61e&",
    "too late": "https://cdn.discordapp.com/attachments/1538562192952266783/1538575627756765186/overdue.gif?ex=6a832db7&is=6a81dc37&hm=77d9c40349d6cc7c2634a4c83bbc98d36a5c8242a396d66b2a6661bb4e95d295&",
    "overdue": "https://cdn.discordapp.com/attachments/1538562192952266783/1538575627756765186/overdue.gif?ex=6a832db7&is=6a81dc37&hm=77d9c40349d6cc7c2634a4c83bbc98d36a5c8242a396d66b2a6661bb4e95d295&",
    "powerdown": "https://cdn.discordapp.com/attachments/1538562192952266783/1538573982066941982/powerdown.gif?ex=6a832c2e&is=6a81daae&hm=54d43134f178ae06502b55284b1f8da6e0f50c7d772471acd4b38608a8452544&",
    "demise": "https://cdn.discordapp.com/attachments/1538562192952266783/1538574264909692958/demise.gif?ex=6a832c72&is=6a81daf2&hm=8b05780065098d1695d49cc94b983f15920509609661d1259d2a11e772517af8&",
    "promotion": "https://cdn.discordapp.com/attachments/1538562192952266783/1538573354964094976/promotion.gif?ex=6a832b99&is=6a81da19&hm=e148160af159b597f97768dc8d0eb4079f9a3979228d530cde3c0cbc280c5f40&",
    "abandoned": "https://cdn.discordapp.com/attachments/1538562192952266783/1538575345710800906/abandoned.gif?ex=6a832d73&is=6a81dbf3&hm=ec12d889fff070d6ad079254142ae90d4453a00f717daa579ff44a6d72c475ef&",
    "the end": "https://cdn.discordapp.com/attachments/1538562192952266783/1538575019989270619/the-end.gif?ex=6a832d26&is=6a81dba6&hm=9be2b19d4c43fe8d87ad7f65e90742073716c7d913a85a93766aab504d9a40ea&",
    "you cannot beat us": "https://cdn.discordapp.com/attachments/1538562192952266783/1538579929111994498/you-cannot-beat-us.gif?ex=6a8331b8&is=6a81e038&hm=9dfeed19d695b8b8d5ac37b1ce2fa09cf1e5bf3b732d932aca25bb3067e84fd0&",
    "unbeatable": "https://cdn.discordapp.com/attachments/1538562192952266783/1538579693593436242/unbeatable.gif?ex=6a833180&is=6a81e000&hm=1f76bb83c1cdbcc0dde6c77a138f29e2628b62498d338530f7ae651f55a8379e&",
    "iason mason": "https://cdn.discordapp.com/attachments/1538562192952266783/1544375439366033508/BAHHH.gif?ex=6a984735&is=6a96f5b5&hm=c96c084c718d6d05b8e8ffa3b8eae48fed5e14a1d9890395c2a135cea66dfeab&",
}

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="/help")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) globally!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    print(f"Logged in as {bot.user.name}!")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    # --- HATE MX TRIGGER ---
    if "i hate mx" in content_lower:
        embed = discord.Embed(color=discord.Color.dark_red())
        # fucking gif link FUCK my life.
        embed.set_image(url="https://cdn.discordapp.com/attachments/1538562192952266783/1543638305621540954/DIE_1.gif?ex=6a9598b3&is=6a944733&hm=3b0f012e0a246fbcad439198a7de494dccb77d03b82a05f5e00f41b68b3ba493&")
        await message.channel.send(embed=embed)
        return

    # --- HATE MX TRIGGER 2 ---
    if "fuck mx" in content_lower:
        embed = discord.Embed(color=discord.Color.dark_red())
        # fucking gif link FUCK my life.
        embed.set_image(url="https://cdn.discordapp.com/attachments/1538562192952266783/1543638305621540954/DIE_1.gif?ex=6a9598b3&is=6a944733&hm=3b0f012e0a246fbcad439198a7de494dccb77d03b82a05f5e00f41b68b3ba493&")
        await message.channel.send(embed=embed)
        return

 # --- HATE MX TRIGGER 2 ---
    if "i love mx" in content_lower:
        embed = discord.Embed(color=discord.Color.dark_red())
        # fucking gif link FUCK my life.
        embed.set_image(url="https://cdn.discordapp.com/attachments/1538562192952266783/1543646444492292166/Video_Project_10.gif?ex=6a95a047&is=6a944ec7&hm=ee56ee878fb23e09eacc59175b7171fa040e779e25b45eec8fc789772f1c2365&")
        await message.channel.send(embed=embed)
        return
    # SONG TRIGGER MESSAGE

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

# --- ASYNC BOT RUNNER ---
def start_bot():
    token = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
    if token:
        asyncio.run(bot.start(token))
    else:
        print("ERROR: DISCORD_TOKEN environment variable is not set!")

# Run Discord bot on a background thread so Flask can immediately bind port 8080
bot_thread = threading.Thread(target=start_bot, daemon=True)
bot_thread.start()

# Main thread runs Flask directly on port 8080 (or Render's PORT)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
