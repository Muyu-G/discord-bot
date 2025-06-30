import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from cogs.database import init_db

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix = ["!"], intents = intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Muyu G"))
    
# syncing slash commands in all the guilds the bot is in
    for guild in bot.guilds:
        await bot.tree.sync(guild=guild)
    print("Slash commands synced!")
    
# loading extensions
    try:
        await bot.load_extension("cogs.mod_commands")
        await bot.load_extension("cogs.infos")
        await bot.load_extension("cogs.n_commands")
    except Exception as e:
        print(f"Failed to load cog: {e}")
        
        
if __name__ == "__main__":
    init_db() #initializing the DB
    bot.run(TOKEN)
