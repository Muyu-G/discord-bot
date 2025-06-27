import discord
from discord.ext import commands
import random

class n_commands (commands.Cog): # n_commands = normal commands like roll etc
    async def roll(self, ctx, sides: int):
        await ctx.send()
    
    

async def setup(bot):
    await bot.add_cog(n_commands(bot))