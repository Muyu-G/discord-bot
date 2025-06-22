import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from database import init_db

init_db()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix = ["g ", "!"], intents = intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Muyu G"))

    for guild in bot.guilds:
        await bot.tree.sync(guild=guild)
    print("Slash commands synced!")

    try:
        await bot.load_extension("cogs.mod_commands")
        await bot.load_extension("cogs.infos")
    except Exception as e:
        print(f"Failed to load cog: {e}")


bot.run(TOKEN)
